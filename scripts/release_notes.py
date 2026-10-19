#!/usr/bin/env python3
"""Write GitHub release notes for one gallery-ai tag.

Each daily release lists only what landed on gallery-ai master since the
previous GitHub release tag: fork commits (first-parent, excluding
``[upstream] Merge gallery-dl master``) and new ``CHANGELOG.md`` version
headers. ``git log A..B`` without ``--first-parent`` walks into those
merges and reprints every upstream commit, so older gallery-dl versions
show up again in later gallery-ai releases.

Examples:

    python3 scripts/release_notes.py \\
        --tag 2026.10.18.061406 --sha HEAD \\
        --prev-tag 2026.10.18.034716
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
UPSTREAM_MERGE_RE = re.compile(r"^\[upstream\] Merge gallery-dl master\b")
CHANGELOG_HEADING_RE = re.compile(r"^## (.+)$")

DEFAULT_FILES = (
    ("gallery-ai_linux", "Linux x86_64 (glibc 2.17+; Debian 12, Ubuntu 22.04)"),
    ("gallery-ai_windows.exe", "Windows x64"),
    ("gallery-ai_macos", "macOS (Apple Silicon)"),
)
LEGACY_FILES = (
    ("gallery-dl_linux", "Linux x86_64"),
    ("gallery-dl_windows.exe", "Windows x64"),
    ("gallery-dl_macos", "macOS (Apple Silicon)"),
)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def is_upstream_merge(subject: str) -> bool:
    return bool(UPSTREAM_MERGE_RE.match(subject.strip()))


def parse_first_parent_log(text: str) -> list[tuple[str, str]]:
    """Parse ``git log --pretty=format:%h%x09%s`` output."""
    entries = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        sha, sep, subject = line.partition("\t")
        if not sep:
            continue
        entries.append((sha.strip(), subject.strip()))
    return entries


def fork_commits(entries: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return [(sha, subject) for sha, subject in entries if not is_upstream_merge(subject)]


def upstream_merge_count(entries: list[tuple[str, str]]) -> int:
    return sum(1 for _, subject in entries if is_upstream_merge(subject))


def changelog_headings(text: str) -> list[str]:
    headings = []
    for line in text.splitlines():
        match = CHANGELOG_HEADING_RE.match(line)
        if not match:
            continue
        headings.append(match.group(1).strip())
    return headings


def new_changelog_headings(previous: str, current: str) -> list[str]:
    seen = set(changelog_headings(previous))
    return [heading for heading in changelog_headings(current) if heading not in seen]


def format_notes(
    *,
    tag: str,
    sha: str,
    repo: str,
    commits: list[tuple[str, str]],
    changelog_versions: list[str],
    prev_tag: str | None,
    files: list[tuple[str, str]] | tuple[tuple[str, str], ...] = DEFAULT_FILES,
    binary_name: str = "gallery-ai",
    initial: bool = False,
    based_on: str | None = None,
    upstream_merges: int = 0,
) -> str:
    lines = [
        f"gallery-ai {tag}",
        "",
        f"Built from https://github.com/{repo}/commit/{sha}",
        "",
        "Standalone executables include a Python interpreter. "
        f"`{binary_name} -U` on these files updates from this repository "
        "(the `dev` channel).",
        "",
        "### Files",
    ]
    for name, desc in files:
        lines.append(f"- `{name}` — {desc}")
    lines.append("")
    if prev_tag:
        lines.append(f"### Changes since {prev_tag}")
    else:
        lines.append("### Changes")
    lines.append("")
    if initial:
        if based_on:
            lines.append(f"Initial gallery-ai release (gallery-dl {based_on}).")
        else:
            lines.append("Initial gallery-ai release.")
        lines.append("")
    if commits:
        for commit_sha, subject in commits:
            lines.append(f"- {subject} (`{commit_sha}`)")
        lines.append("")
    if changelog_versions:
        lines.append("Merged gallery-dl:")
        for heading in changelog_versions:
            lines.append(f"- {heading}")
        lines.append("")
    elif upstream_merges and not initial:
        noun = "commit" if upstream_merges == 1 else "commits"
        lines.append(f"Merged gallery-dl master ({upstream_merges} {noun}).")
        lines.append("")
    if not commits and not changelog_versions and not upstream_merges and not initial:
        lines.append("No listed changes.")
        lines.append("")
    if prev_tag:
        lines.append(f"https://github.com/{repo}/compare/{prev_tag}...{tag}")
        lines.append("")
    return "\n".join(lines)


def git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def rev_exists(rev: str, cwd: Path) -> bool:
    result = git(["rev-parse", "--verify", f"{rev}^{{}}"], cwd)
    return result.returncode == 0


def show_file(rev: str, path: str, cwd: Path) -> str:
    result = git(["show", f"{rev}:{path}"], cwd)
    if result.returncode != 0:
        return ""
    return result.stdout


def collect_log(since: str, sha: str, cwd: Path) -> list[tuple[str, str]]:
    result = git(
        ["log", "--first-parent", "--pretty=format:%h%x09%s", f"{since}..{sha}"],
        cwd,
    )
    if result.returncode != 0:
        eprint(result.stderr.strip() or f"git log {since}..{sha} failed")
        return []
    return parse_first_parent_log(result.stdout)


def resolve_sha(sha: str, cwd: Path) -> str:
    result = git(["rev-parse", "--verify", f"{sha}^{{}}"], cwd)
    if result.returncode != 0:
        return sha
    return result.stdout.strip()


def build_notes(
    *,
    tag: str,
    sha: str,
    repo: str,
    prev_tag: str | None,
    since: str | None,
    cwd: Path,
    files: list[tuple[str, str]] | tuple[tuple[str, str], ...],
    binary_name: str,
) -> str:
    full_sha = resolve_sha(sha, cwd)
    range_start = since or prev_tag
    entries: list[tuple[str, str]] = []
    current_changelog = show_file(sha, "CHANGELOG.md", cwd)
    previous_changelog = ""
    initial = not prev_tag

    if range_start and rev_exists(range_start, cwd) and rev_exists(sha, cwd):
        entries = collect_log(range_start, sha, cwd)
        if prev_tag and rev_exists(prev_tag, cwd):
            previous_changelog = show_file(prev_tag, "CHANGELOG.md", cwd)
        elif since and rev_exists(since, cwd):
            previous_changelog = show_file(since, "CHANGELOG.md", cwd)

    versions: list[str] = []
    if previous_changelog:
        versions = new_changelog_headings(previous_changelog, current_changelog)
    based_on = None
    if initial:
        headings = changelog_headings(current_changelog)
        based_on = headings[0].split(" - ", 1)[0] if headings else None

    return format_notes(
        tag=tag,
        sha=full_sha,
        repo=repo,
        commits=fork_commits(entries),
        changelog_versions=versions,
        prev_tag=prev_tag,
        files=files,
        binary_name=binary_name,
        initial=initial,
        based_on=based_on,
        upstream_merges=upstream_merge_count(entries),
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True, help="GitHub release tag")
    parser.add_argument("--sha", default="HEAD", help="Release commit (default HEAD)")
    parser.add_argument("--prev-tag", default="", help="Previous GitHub release tag")
    parser.add_argument(
        "--since",
        default="",
        help="Git revision to start the first-parent log at (default: --prev-tag)",
    )
    parser.add_argument("--repo", default="CrimsonGlory/gallery-ai")
    parser.add_argument(
        "--files",
        choices=("gallery-ai", "gallery-dl"),
        default="gallery-ai",
        help="Asset names in the Files section",
    )
    parser.add_argument(
        "--binary-name",
        default="",
        help="Executable name used in the -U text (default: --files)",
    )
    parser.add_argument(
        "--git-dir",
        default=str(REPO),
        help="Repository working tree",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    cwd = Path(args.git_dir)
    prev_tag = args.prev_tag.strip() or None
    since = args.since.strip() or None
    files = DEFAULT_FILES if args.files == "gallery-ai" else LEGACY_FILES
    binary_name = args.binary_name.strip() or args.files
    sys.stdout.write(
        build_notes(
            tag=args.tag,
            sha=args.sha,
            repo=args.repo,
            prev_tag=prev_tag,
            since=since,
            cwd=cwd,
            files=files,
            binary_name=binary_name,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
