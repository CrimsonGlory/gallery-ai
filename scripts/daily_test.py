#!/usr/bin/env python3
"""Daily unit + live extractor run: Docker, log results, Grok-fix, push.

Runs ``scripts/run_tests.py`` then ``test/test_results.py`` in Docker. Parses
unittest output, then launches one ``grok`` process when anything failed.
Grok commits; this script pushes when the branch is ahead of origin.

Intended to be run once a day from cron via ./daily_test.sh (flock + logs).

Examples:

    python3 scripts/daily_test.py --dry-run
    python3 scripts/daily_test.py --no-grok
    python3 scripts/daily_test.py --from-log tmp/daily-test/live-latest.log
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROMPT_TEMPLATE = Path(__file__).resolve().parent / "daily_test.prompt.md"
DEFAULT_LOG_DIR = REPO / "tmp" / "daily-test"
PROGRESS_NAME = "progress.jsonl"
DEFAULT_IMAGE = os.environ.get("GALLERY_AI_TEST_IMAGE", "gallery-ai:latest")

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
FAIL_LINE_RE = re.compile(r"^(FAIL|ERROR): (.+)$")
RAN_RE = re.compile(r"^Ran (\d+) tests in ([\d.]+)s$")
FAILED_PAREN_RE = re.compile(r"^FAILED \((.*)\)$")
OK_RE = re.compile(r"^OK(?: \((.*)\))?$")
COUNT_PAIR_RE = re.compile(r"(\w+)=(\d+)")
SEP_RE = re.compile(r"^={10,}\s*$")


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Run Docker unit+live tests, Grok-fix failures, push.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR,
                   help="Where to write test logs, prompt, grok log, progress")
    p.add_argument("--image", default=DEFAULT_IMAGE,
                   help="Docker image (default: gallery-ai:latest)")
    p.add_argument("--config-dir", type=Path,
                   default=Path(os.environ["GALLERY_AI_CONFIG_DIR"])
                   if os.environ.get("GALLERY_AI_CONFIG_DIR")
                   else Path.home() / ".config" / "gallery-dl",
                   help="Host gallery-dl config dir mounted into the container")
    p.add_argument("--from-log", type=Path,
                   help="Skip the suite; parse this existing live/unit log")
    p.add_argument("--unit-only", action="store_true",
                   help="Run only scripts/run_tests.py")
    p.add_argument("--live-only", action="store_true",
                   help="Run only test/test_results.py")
    p.add_argument("--dry-run", action="store_true",
                   help="Run/parse tests and write the prompt; do not invoke Grok")
    p.add_argument("--no-grok", action="store_true",
                   help="Never invoke Grok, even if tests failed")
    p.add_argument("--no-commit", action="store_true",
                   help="Tell Grok not to commit (default: commit on success)")
    p.add_argument("--no-push", action="store_true",
                   help="Do not git push after the run")
    p.add_argument("--rebuild-image", action="store_true",
                   help="docker build -t IMAGE . before the suite")
    p.add_argument("--unit-timeout", type=int, default=600,
                   help="Seconds for the unit suite (0 = no limit)")
    p.add_argument("--test-timeout", type=int, default=14400,
                   help="Seconds for the live suite (0 = no limit; default 4h)")
    p.add_argument("--timeout", type=int, default=14400,
                   help="Seconds for the Grok invocation (0 = no limit; default 4h)")
    p.add_argument("--max-turns", type=int, default=200, help="Grok --max-turns")
    p.add_argument("--max-failures", type=int, default=60,
                   help="Max failing test names to embed in the Grok prompt")
    p.add_argument("--grok-bin", default=os.environ.get("GROK_BIN", "grok"),
                   help="Grok executable")
    p.add_argument("--model", default=os.environ.get("GROK_MODEL", ""),
                   help="Optional grok --model")
    p.add_argument("--grok-arg", action="append", default=[],
                   help="Extra arg passed through to grok (repeatable)")
    return p.parse_args(argv)


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text.replace("\r", ""))


def git(args: list[str], check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(REPO),
        text=True,
        capture_output=True,
        check=check,
    )


def git_out(args: list[str]) -> str:
    proc = git(args)
    if proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{(proc.stderr or proc.stdout).strip()}")
    return (proc.stdout or "").strip()


def merge_in_progress() -> bool:
    return (REPO / ".git" / "MERGE_HEAD").exists()


def last_lines(text: str, n: int = 16) -> str:
    lines = [ln.rstrip() for ln in strip_ansi(text).splitlines()]
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines[-n:])


def _paren_counts(body: str) -> dict:
    counts = {"failures": 0, "errors": 0, "skipped": 0, "expected failures": 0}
    for key, val in COUNT_PAIR_RE.findall(body or ""):
        if key in counts:
            counts[key] = int(val)
        elif key == "unexpected successes":
            counts["failures"] = counts.get("failures", 0) + int(val)
    return counts


def parse_unittest_log(text: str) -> dict:
    """Parse unittest TextTestRunner stdout for summary and FAIL/ERROR names."""
    lines = [strip_ansi(ln).rstrip() for ln in text.splitlines()]
    ran = None
    seconds = None
    failed = errors = skipped = passed = 0
    summary_line = ""
    ok = False

    for ln in reversed(lines):
        s = ln.strip()
        if not s:
            continue
        m_fail = FAILED_PAREN_RE.match(s)
        if m_fail:
            counts = _paren_counts(m_fail.group(1))
            failed = counts["failures"]
            errors = counts["errors"]
            skipped = counts["skipped"]
            summary_line = s
            continue
        m_ok = OK_RE.match(s)
        if m_ok:
            ok = True
            if m_ok.group(1):
                skipped = _paren_counts(m_ok.group(1))["skipped"]
            summary_line = s
            continue
        m_ran = RAN_RE.match(s)
        if m_ran:
            ran = int(m_ran.group(1))
            seconds = m_ran.group(2)
            if summary_line:
                summary_line = f"{s}\n{summary_line}"
            else:
                summary_line = s
            break

    failed_tests: list[str] = []
    error_tests: list[str] = []
    for ln in lines:
        m = FAIL_LINE_RE.match(ln.strip())
        if not m:
            continue
        name = m.group(2).strip()
        if m.group(1) == "FAIL":
            if name not in failed_tests:
                failed_tests.append(name)
        elif name not in error_tests:
            error_tests.append(name)

    if ran is not None:
        passed = max(0, ran - failed - errors - skipped)
    elif ok:
        passed = max(0, len([ln for ln in lines if ln.strip() == "ok"]) or 0)

    duration = f"{seconds}s" if seconds else ""
    all_failed = failed_tests + error_tests
    return {
        "summary_line": summary_line,
        "ran": ran,
        "failed": failed if summary_line else len(failed_tests),
        "errors": errors if summary_line else len(error_tests),
        "passed": passed,
        "skipped": skipped,
        "duration": duration,
        "failed_tests": failed_tests,
        "error_tests": error_tests,
        "all_failed": all_failed,
        "tail": last_lines(text, 16),
    }


def format_failed_tests(names: list[str], limit: int) -> str:
    if not names:
        return "(none parsed — read the log tail)"
    shown = names[:limit]
    lines = [f"{i}. `{n}`" for i, n in enumerate(shown, 1)]
    hidden = len(names) - len(shown)
    if hidden > 0:
        lines.append(f"… and {hidden} more (see the log)")
    return "\n".join(lines)


def format_excerpts(log_text: str, names: list[str],
                    limit: int, per_item: int = 2500) -> str:
    """Pull unittest FAIL/ERROR blocks that follow a '====' separator."""
    lines = [strip_ansi(ln).rstrip("\n") for ln in log_text.splitlines()]
    chunks: list[str] = []
    i = 0
    wanted = set(names[:limit]) if names else None
    while i < len(lines) and len(chunks) < limit:
        if not SEP_RE.match(lines[i].strip()):
            i += 1
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j >= len(lines):
            break
        header = lines[j].strip()
        m = FAIL_LINE_RE.match(header)
        if not m:
            i += 1
            continue
        name = m.group(2).strip()
        k = j + 1
        while k < len(lines) and not SEP_RE.match(lines[k].strip()):
            k += 1
        body = "\n".join(lines[i:k]).strip()
        i = k
        if wanted is not None and name not in wanted and names:
            # still take it if we have room and nothing else matched yet
            if chunks or len(names) > limit:
                continue
        if len(body) > per_item:
            body = body[:per_item] + "\n… (truncated)"
        chunks.append(f"### `{name}`\n```\n{body}\n```")
    if not chunks:
        return "(no excerpts; open the log)"
    return "\n\n".join(chunks)


def empty_result() -> dict:
    return {
        "summary_line": "(not run)",
        "ran": 0,
        "failed": 0,
        "errors": 0,
        "passed": 0,
        "skipped": 0,
        "duration": "",
        "failed_tests": [],
        "error_tests": [],
        "all_failed": [],
        "tail": "",
        "exit": 0,
        "log": "",
        "cmd": "",
        "elapsed_s": 0.0,
    }


def docker_prefix(args) -> list[str]:
    uid = os.getuid()
    gid = os.getgid()
    cmd = [
        "docker", "run", "--rm",
        "--user", f"{uid}:{gid}",
        "--entrypoint", "python3",
        "-v", f"{REPO}:/src",
        "-w", "/src",
        "-e", "PYTHONPATH=/src",
        "-e", "PYTHONUNBUFFERED=1",
        "-e", "HOME=/tmp",
    ]
    cfg = args.config_dir
    if cfg is not None and Path(cfg).is_dir():
        cmd.extend(["-v", f"{Path(cfg).resolve()}:/tmp/.config/gallery-dl:ro"])
    cmd.append(args.image)
    cmd.extend(["-u"])
    return cmd


def docker_cmd_str(args, script: str) -> str:
    return " ".join(docker_prefix(args) + [script])


def image_exists(image: str) -> bool:
    proc = subprocess.run(
        ["docker", "image", "inspect", image],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc.returncode == 0


def ensure_image(args) -> int:
    if args.rebuild_image or not image_exists(args.image):
        eprint(f"Building Docker image {args.image} …")
        proc = subprocess.run(
            ["docker", "build", "-t", args.image, "."],
            cwd=str(REPO),
        )
        return proc.returncode
    return 0


def _killpg(proc: subprocess.Popen) -> None:
    if proc.poll() is None:
        with contextlib.suppress(ProcessLookupError):
            os.killpg(proc.pid, signal.SIGTERM)


def run_logged(cmd: list[str], log_file: Path, timeout: int,
               env: dict | None = None) -> int:
    """Run cmd, tee stdout+stderr to log_file and this process's stdout."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    eprint("+", " ".join(cmd))
    with log_file.open("w", encoding="utf-8") as log:
        log.write("# cmd: " + " ".join(cmd) + "\n\n")
        log.flush()
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(REPO),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                start_new_session=True,
                env=env,
            )
        except FileNotFoundError:
            eprint(f"error: {cmd[0]!r} not found on PATH.")
            return 127

        old_int = signal.signal(signal.SIGINT, lambda *_: _killpg(proc))
        try:
            deadline = time.monotonic() + timeout if timeout else None
            assert proc.stdout is not None
            while True:
                if deadline is not None and time.monotonic() > deadline:
                    eprint(f"error: timed out after {timeout}s: {cmd[0]}")
                    _killpg(proc)
                    try:
                        proc.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        os.killpg(proc.pid, signal.SIGKILL)
                    return 124
                line = proc.stdout.readline()
                if line == "" and proc.poll() is not None:
                    break
                if line:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                    log.write(line)
            return proc.wait()
        finally:
            signal.signal(signal.SIGINT, old_int)


def point_latest(log_dir: Path, latest_name: str, target: Path) -> None:
    latest = log_dir / latest_name
    try:
        if latest.exists() or latest.is_symlink():
            latest.unlink()
        latest.symlink_to(target.name)
    except OSError:
        shutil.copyfile(target, latest)


def grok_cmd(args, prompt_file: Path) -> list[str]:
    cmd = [
        args.grok_bin,
        "--prompt-file", str(prompt_file),
        "--verbatim",
        "--always-approve",
        "--permission-mode", "bypassPermissions",
        "--cwd", str(REPO),
        "--no-memory",
        "--no-plan",
        "--no-alt-screen",
        "--output-format", "plain",
        "--max-turns", str(args.max_turns),
    ]
    if args.model:
        cmd.extend(["--model", args.model])
    cmd.extend(args.grok_arg)
    return cmd


def parse_status_from_log(log_file: Path) -> str | None:
    if not log_file.is_file():
        return None
    text = log_file.read_text(encoding="utf-8", errors="replace")
    for token in (
        "STATUS: FIXED",
        "STATUS: PARTIAL",
        "STATUS: BLOCKED",
        "STATUS: FAILED",
        "STATUS: PASSED",
    ):
        if token in text:
            return token.split()[-1]
    return None


def append_progress(path: Path, rec: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def build_prompt(
    template: str,
    *,
    today: str,
    branch: str,
    head: str,
    image: str,
    unit: dict,
    live: dict,
    excerpts: str,
    log_tail: str,
    do_commit: bool,
    max_failures: int,
) -> str:
    if do_commit:
        commit_instruction = (
            "- After you have actually re-run the failing modules you claim to "
            "have fixed, git-add **only** those files (extractor(s), "
            "`test/results/*.py`, `test/test_*.py`, `gallery_dl/http.py` if you "
            "touched it) and create **one** commit:\n"
            "  `[daily-test] Fix <N> failing tests`\n"
            "  Body: bullet per extractor/test, complete sentences.\n"
            "- A second commit is OK if unit and live are separate. "
            "Do not `git add -A`. Do not amend. Do not push.\n"
            "- If you fixed nothing, do not commit."
        )
    else:
        commit_instruction = (
            "- Do **not** git commit, amend, or push. Leave the working tree "
            "dirty for review. (Operator passed --no-commit.)"
        )
    replacements = {
        "__TODAY__": today,
        "__BRANCH__": branch,
        "__HEAD__": head,
        "__DOCKER_IMAGE__": image,
        "__UNIT_CMD__": unit.get("cmd") or "(skipped)",
        "__LIVE_CMD__": live.get("cmd") or "(skipped)",
        "__UNIT_EXIT__": str(unit.get("exit", 0)),
        "__LIVE_EXIT__": str(live.get("exit", 0)),
        "__UNIT_SUMMARY__": unit.get("summary_line") or "(none)",
        "__LIVE_SUMMARY__": live.get("summary_line") or "(none)",
        "__UNIT_FAILED__": str(unit.get("failed", 0)),
        "__UNIT_ERRORS__": str(unit.get("errors", 0)),
        "__UNIT_PASSED__": str(unit.get("passed", 0)),
        "__UNIT_SKIPPED__": str(unit.get("skipped", 0)),
        "__LIVE_FAILED__": str(live.get("failed", 0)),
        "__LIVE_ERRORS__": str(live.get("errors", 0)),
        "__LIVE_PASSED__": str(live.get("passed", 0)),
        "__LIVE_SKIPPED__": str(live.get("skipped", 0)),
        "__UNIT_DURATION__": unit.get("duration") or "unknown",
        "__LIVE_DURATION__": live.get("duration") or "unknown",
        "__UNIT_LOG__": unit.get("log") or "(none)",
        "__LIVE_LOG__": live.get("log") or "(none)",
        "__LOG_TAIL__": log_tail or "(empty)",
        "__UNIT_FAILED_TESTS__": format_failed_tests(
            unit.get("all_failed") or [], max_failures),
        "__LIVE_FAILED_TESTS__": format_failed_tests(
            live.get("all_failed") or [], max_failures),
        "__FAILURE_EXCERPTS__": excerpts or "(none)",
        "__COMMIT_INSTRUCTION__": commit_instruction,
    }
    out = template
    for key, value in replacements.items():
        out = out.replace(key, value)
    return out


def needs_grok(unit: dict, live: dict) -> bool:
    for result in (unit, live):
        if result.get("exit", 0) not in (0, None):
            return True
        if (result.get("failed", 0) + result.get("errors", 0)) > 0:
            return True
        if result.get("all_failed"):
            return True
    return False


def report_result(label: str, result: dict) -> None:
    eprint("")
    eprint(f"=== {label} ===")
    if result.get("summary_line"):
        eprint(result["summary_line"])
    eprint(
        f"exit={result.get('exit')}  failed={result.get('failed')}  "
        f"errors={result.get('errors')}  passed={result.get('passed')}  "
        f"skipped={result.get('skipped')}  duration={result.get('duration') or '?'}",
    )
    names = result.get("all_failed") or []
    if names:
        eprint(f"failed tests ({len(names)}):")
        for name in names[:30]:
            eprint(f"  {name}")
        extra = len(names) - 30
        if extra > 0:
            eprint(f"  … and {extra} more")
    elif result.get("exit"):
        eprint("no FAIL/ERROR names parsed; last lines:")
        eprint(result.get("tail") or "(empty)")
    eprint("===================")


def run_suite(args, script: str, log_file: Path, timeout: int) -> dict:
    cmd = docker_prefix(args) + [script]
    t0 = time.time()
    rc = run_logged(cmd, log_file, timeout)
    elapsed = round(time.time() - t0, 1)
    text = log_file.read_text(encoding="utf-8", errors="replace")
    parsed = parse_unittest_log(text)
    parsed["exit"] = rc
    parsed["log"] = str(log_file)
    parsed["cmd"] = " ".join(cmd)
    parsed["elapsed_s"] = elapsed
    if parsed["failed"] + parsed["errors"] > 0 and rc == 0:
        parsed["exit"] = 1
    return parsed


def push_if_ahead() -> int:
    proc = git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    if proc.returncode != 0:
        eprint("No upstream tracking branch; git push -u origin HEAD")
        push = subprocess.run(
            ["git", "push", "-u", "origin", "HEAD"],
            cwd=str(REPO),
        )
        return push.returncode
    try:
        ahead = int(git_out(["rev-list", "--count", "@{u}..HEAD"]))
    except (RuntimeError, ValueError):
        ahead = 0
    if ahead <= 0:
        eprint("Nothing to push (branch is not ahead of origin).")
        return 0
    upstream = (proc.stdout or "").strip()
    eprint(f"Pushing {ahead} commit(s) to {upstream}")
    push = subprocess.run(["git", "push"], cwd=str(REPO))
    return push.returncode


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.unit_only and args.live_only:
        eprint("error: --unit-only and --live-only are mutually exclusive")
        return 2
    if not PROMPT_TEMPLATE.is_file():
        eprint(f"error: prompt template not found: {PROMPT_TEMPLATE}")
        return 2
    if not (REPO / ".git").exists():
        eprint(f"error: not a git checkout: {REPO}")
        return 2

    args.log_dir.mkdir(parents=True, exist_ok=True)
    (args.log_dir / "grok").mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    stamp = time.strftime("%Y-%m-%dT%H%M%S")

    try:
        branch = git_out(["rev-parse", "--abbrev-ref", "HEAD"])
        head = git_out(["rev-parse", "HEAD"])
    except RuntimeError as exc:
        eprint(f"error: {exc}")
        return 2

    if merge_in_progress():
        eprint("warning: MERGE_HEAD exists; a merge is in progress")

    unit = empty_result()
    live = empty_result()

    if args.from_log is not None:
        log_path = args.from_log.resolve()
        if not log_path.is_file():
            eprint(f"error: --from-log not found: {log_path}")
            return 2
        eprint(f"Reusing log: {log_path}")
        text = log_path.read_text(encoding="utf-8", errors="replace")
        parsed = parse_unittest_log(text)
        parsed["exit"] = 1 if (parsed["failed"] + parsed["errors"]) else 0
        parsed["log"] = str(log_path)
        parsed["cmd"] = "(from --from-log)"
        if "test_results" in log_path.name or "live" in log_path.name:
            live = parsed
        else:
            unit = parsed
    else:
        if shutil.which("docker") is None:
            eprint("error: docker not found on PATH")
            return 2
        build_rc = ensure_image(args)
        if build_rc != 0:
            eprint(f"error: docker build failed ({build_rc})")
            return build_rc

        if not args.live_only:
            unit_log = args.log_dir / f"unit-{stamp}.log"
            unit = run_suite(
                args, "scripts/run_tests.py", unit_log, args.unit_timeout)
            point_latest(args.log_dir, "unit-latest.log", unit_log)
            report_result("unit", unit)

        if not args.unit_only:
            live_log = args.log_dir / f"live-{stamp}.log"
            live = run_suite(
                args, "test/test_results.py", live_log, args.test_timeout)
            point_latest(args.log_dir, "live-latest.log", live_log)
            report_result("live", live)

    if args.from_log:
        report_result("from-log", live if live.get("log") else unit)

    grok_wanted = needs_grok(unit, live)
    progress_path = args.log_dir / PROGRESS_NAME
    log_tail = live.get("tail") or unit.get("tail") or ""

    summary_rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "stamp": stamp,
        "branch": branch,
        "head": head,
        "image": args.image,
        "unit_exit": unit.get("exit"),
        "live_exit": live.get("exit"),
        "unit_failed": unit.get("failed"),
        "unit_errors": unit.get("errors"),
        "live_failed": live.get("failed"),
        "live_errors": live.get("errors"),
        "unit_log": unit.get("log"),
        "live_log": live.get("log"),
    }
    summary_path = args.log_dir / f"summary-{stamp}.json"
    summary_path.write_text(
        json.dumps(summary_rec, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    eprint(f"Summary: {summary_path}")

    def finish(status: str, exit_code: int, extra: dict | None = None) -> int:
        rec = {
            "status": status,
            "exit_code": exit_code,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            **{k: summary_rec[k] for k in (
                "stamp", "head", "unit_exit", "live_exit",
                "unit_failed", "live_failed", "unit_log", "live_log")},
        }
        if extra:
            rec.update(extra)
        try:
            rec["head_after"] = git_out(["rev-parse", "HEAD"])
        except RuntimeError:
            rec["head_after"] = None
        push_rc = 0
        if not args.dry_run and not args.no_push:
            push_rc = push_if_ahead()
            rec["push_exit"] = push_rc
        else:
            rec["push_exit"] = None
        append_progress(progress_path, rec)
        if push_rc not in (0, None) and exit_code == 0:
            return push_rc
        return exit_code

    if not grok_wanted:
        eprint("Suite passed. Skipping Grok.")
        return finish("PASSED", 0)

    if args.no_grok:
        eprint("--no-grok: not invoking Grok")
        return finish("FAILED", unit.get("exit") or live.get("exit") or 1,
                      {"skipped_grok": True})

    if merge_in_progress():
        eprint("error: merge in progress; refusing to launch Grok (STATUS: BLOCKED)")
        return finish("BLOCKED", 3, {"reason": "MERGE_HEAD"})

    unit_text = ""
    live_text = ""
    if unit.get("log") and Path(unit["log"]).is_file():
        unit_text = Path(unit["log"]).read_text(encoding="utf-8", errors="replace")
    if live.get("log") and Path(live["log"]).is_file():
        live_text = Path(live["log"]).read_text(encoding="utf-8", errors="replace")
    excerpts_parts = []
    if live_text:
        excerpts_parts.append(format_excerpts(
            live_text, live.get("all_failed") or [], args.max_failures))
    if unit_text:
        excerpts_parts.append(format_excerpts(
            unit_text, unit.get("all_failed") or [], args.max_failures))
    excerpts = "\n\n".join(p for p in excerpts_parts if p)

    template = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    prompt = build_prompt(
        template,
        today=today,
        branch=branch,
        head=head,
        image=args.image,
        unit=unit,
        live=live,
        excerpts=excerpts,
        log_tail=log_tail,
        do_commit=not args.no_commit,
        max_failures=args.max_failures,
    )
    prompt_file = args.log_dir / f"prompt-{stamp}.txt"
    prompt_file.write_text(prompt, encoding="utf-8")
    eprint(f"Wrote prompt: {prompt_file}")
    n_fail = len(unit.get("all_failed") or []) + len(live.get("all_failed") or [])
    eprint(f"Grok will see up to {args.max_failures} names from {n_fail} failures")

    if args.dry_run:
        eprint("dry-run: would exec:", " ".join(grok_cmd(args, prompt_file)[:8]), "…")
        rec = {
            "status": "DRY_RUN",
            "exit_code": 0,
            "ts": summary_rec["ts"],
            "prompt": str(prompt_file),
            "unit_failed": unit.get("failed"),
            "live_failed": live.get("failed"),
            "push_exit": None,
        }
        append_progress(progress_path, rec)
        return 0

    grok_log = args.log_dir / "grok" / f"{stamp}.log"
    t0 = time.time()
    rc = run_logged(grok_cmd(args, prompt_file), grok_log, args.timeout)
    elapsed = round(time.time() - t0, 1)
    status = parse_status_from_log(grok_log)
    if rc == 130:
        status = status or "ERROR"
    elif rc != 0 and not status:
        status = "ERROR"
    elif not status:
        status = "FAILED"

    eprint(f"-- grok status={status} exit={rc} elapsed={elapsed}s")
    eprint(f"Grok log: {grok_log}")

    grok_exit = 0
    if rc == 130:
        grok_exit = 130
    elif status in ("FIXED", "PARTIAL") and rc == 0:
        grok_exit = 0
    elif status == "BLOCKED":
        grok_exit = 3
    else:
        grok_exit = 1 if rc == 0 else rc

    return finish(status, grok_exit, {
        "elapsed_s": elapsed,
        "log": str(grok_log),
        "prompt": str(prompt_file),
        "failed_tests": (unit.get("all_failed") or []) + (live.get("all_failed") or []),
    })


if __name__ == "__main__":
    raise SystemExit(main())
