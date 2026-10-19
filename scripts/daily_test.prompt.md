You are working in the gallery-ai git checkout at the current working directory.

The daily test run failed. Fix **every listed failing test**, then **commit**. Do not wait for a human. Do not push (the wrapper script pushes after you finish).

Today's date: __TODAY__
Current branch: `__BRANCH__`
Current HEAD: `__HEAD__`
Docker image: `__DOCKER_IMAGE__`
Unit command: `__UNIT_CMD__`
Live command: `__LIVE_CMD__`
Unit exit: `__UNIT_EXIT__`  Live exit: `__LIVE_EXIT__`

## What this repo is

gallery-ai is **gallery-dl plus more**. Package stays `gallery_dl`. Extra sites and working result tests stay. Prefer Docker for tests (image `__DOCKER_IMAGE__`). Mount is `/src`, `PYTHONPATH=/src`, override entrypoint to `python3`.

## Suite result

Unit summary:

```
__UNIT_SUMMARY__
```

Live summary:

```
__LIVE_SUMMARY__
```

Counts: unit failed=__UNIT_FAILED__ errors=__UNIT_ERRORS__ passed=__UNIT_PASSED__ skipped=__UNIT_SKIPPED__
live failed=__LIVE_FAILED__ errors=__LIVE_ERRORS__ passed=__LIVE_PASSED__ skipped=__LIVE_SKIPPED__
duration unit=__UNIT_DURATION__ live=__LIVE_DURATION__

Unit log: `__UNIT_LOG__`
Live log: `__LIVE_LOG__`

Last lines of the live log (or unit log if live was skipped):

```
__LOG_TAIL__
```

## Failing unit tests

__UNIT_FAILED_TESTS__

## Failing live tests

__LIVE_FAILED_TESTS__

## Failure excerpts

__FAILURE_EXCERPTS__

## Goal

1. Make every listed failure pass, or mark a **gone URL** with `#exception` after you proved it (see below).
2. Re-run **only** the failing unit modules / live result modules. Do **not** re-run the full live suite — it takes ~3 hours. Tomorrow's cron will.
3. Commit the fixes. Never push.

A PARTIAL result (some tests fixed and committed, some remaining) is acceptable. An empty commit is not.

If you cannot reproduce a failure (transient 5xx / timeout / DNS) after **two** retries of that single test, leave it and note it as remaining. Do not skip a test because it flaked once.

## How to work

### 0. Safety

- Stay on `__BRANCH__`. Do not checkout a new branch. Do not rebase. Do not `reset --hard`. Do not `git add -A` (the tree may have untracked downloads).
- Do not push. Do not amend published commits.
- Do not commit downloaded images, archives, `*.part` files, logs, or anything under `tmp/`.
- This tree still supports **Python 3.8**. Do not drop 3.8.
- Never add DRM circumvention, credential-stealing, or supply-chain surprises.
- Follow `AGENTS.md`. Prefer Docker for re-runs:

```
docker run --rm --entrypoint python3 \
  -v "$PWD":/src -w /src -e PYTHONPATH=/src -e PYTHONUNBUFFERED=1 \
  __DOCKER_IMAGE__ -u scripts/run_tests.py
```

```
docker run --rm --entrypoint python3 \
  -v "$PWD":/src -w /src -e PYTHONPATH=/src -e PYTHONUNBUFFERED=1 \
  __DOCKER_IMAGE__ -u test/test_results.py <module>
```

`<module>` is the `test/results/<module>.py` **filename stem**, not the `#category` tuple. Dots are stripped (`mastodon.social` → try `mastodonsocial` or `mastodon`). Hyphens stay (`bbw-chan`). `hentaiimg` / `pornimage` live in `hentaicosplays.py`. `naver-webtoon` is `naverwebtoon`.

### 1. Classify each failure

Work through the list **one test / one results module at a time**.

| Kind | What to do |
| --- | --- |
| Unit (`test/test_*.py` other than `test_results.py`) | Real bug. Fix the code or the assertion. Do not skip. |
| Live, stale metadata / counts / hashes | Update `test/results/<module>.py`. Prefer `str` / `int` / `list` / `{int, None}` / `type:datetime` / `re:` / `?optional` over chasing a snapshot that changes daily. Keep a true live URL. |
| Live, extractor bug (`TypeError`, `KeyError`, `AbortExtraction: None`, empty `"None"` query params) | Fix `gallery_dl/extractor/` or HTTP. `curl_cffi` sends the literal `"None"` unless missing values are dropped (`gallery_dl/http.py`). |
| Live, gone URL (404 / `NotFoundError`) | `#exception: exception.NotFoundError` on **that** test. Do not skip 404 globally. Find a replacement public URL on the same site when one exists, and keep the gone URL as `#exception` in addition. |
| Live, WAF / 401 / 403 / 429 / DNS / TLS / 5xx | The harness already skips these (`_ENV_HTTP` / `_ENV_ABORT`). Do not add a blanket skip. If it still fails, leave it remaining. |
| Live, login / cookies / paid | Only after you proved it. `#auth: True` skips when credentials are missing. Do not delete the extractor. |
| Hung / `TestTimeout` | Harness already time-boxes a single URL (~10 min). Do not ignore a hang that is an extractor bug (unbounded pagination, missing stop). |

**Not a fix** (do not do these):

- Empty SHA1 `da39a3ee5e6b4b0d3255bfef95601890afd80709` for `#sha1_url` or `#sha1_content`
- `#count: ">= 0"` or a range that accepts **zero** plus a `#pattern` (pattern requires at least one URL)
- Vacuous `#pattern: r"https?://.+"`
- Skipping `AbortExtraction` 400 globally (that hid real `None` bugs)
- Skipping 404 globally

`#pattern` as a string requires `len(url_list) > 0`. Optional metadata keys use a `?` prefix. `#results` is exact URL match (`re:` prefix is **not** regex for `#results`). `#log` with a leading `~` allows extra log lines.

### 2. Reproduce one failure

Unit:

```
docker run --rm --entrypoint python3 \
  -v "$PWD":/src -w /src -e PYTHONPATH=/src \
  __DOCKER_IMAGE__ -u scripts/run_tests.py test_<module>
```

Live, one results module:

```
docker run --rm --entrypoint python3 \
  -v "$PWD":/src -w /src -e PYTHONPATH=/src \
  __DOCKER_IMAGE__ -u test/test_results.py <module>
```

Read the traceback in the log. unittest `assertEqual(expected, actual)` so `A != B` means the fixture expected A and live produced B.

### 3. Smallest fix, then re-run that module

- Extractor logic: keep extra URL patterns and result tests this fork already has.
- Fixture-only: types/ranges/regex/`?` optional keys for fields that drift; `#exception` for gone URLs.
- Do not regenerate `docs/supportedsites.md` unless you added or removed an extractor module.

### 4. Commit

__COMMIT_INSTRUCTION__

## Constraints

- Touch only files needed for these failures.
- Do not refactor unrelated extractors.
- Do not re-run the full live suite.
- Do not push.
- Do not invent a fake pass.

## When you are done

Print exactly this block (fill it in):

```
STATUS: FIXED | PARTIAL | FAILED | BLOCKED
FIXED: <comma-separated test names or modules now passing, or none>
REMAINING: <comma-separated still-failing tests, or none>
COMMIT: <commit sha, or none>
NOTES: <2-5 sentences: what was wrong, what you changed, what you left>
```
