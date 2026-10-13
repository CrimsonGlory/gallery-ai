# Project rules

## Environment

Prefer Docker for all work in this repo: tests, scripts, installs, and other tooling. Do not run them on the host when a container can do it.

Use the repo `Dockerfile` (`python:3.14-alpine`, deps from `requirements/docker`). The image `ENTRYPOINT` is `gallery-dl` and it installs upstream gallery-dl, not this checkout. For local code, mount the repo, set `PYTHONPATH` to that mount, and override the entrypoint.

Build once (repeat when the Dockerfile or requirements change):

```bash
docker build -t gallery-dl:test .
```

## Tests

Full unit suite (`scripts/run_tests.py`). This loads every `test/test_*.py` module except the live extractor check `test/test_results.py`.

```bash
docker run --rm --entrypoint python3 \
  -v "$PWD":/src -w /src -e PYTHONPATH=/src \
  gallery-dl:test scripts/run_tests.py
```

## Releases

Daily GitHub releases are dispatched by `./release.sh` (same pattern as yt-ai).
It triggers the `Release` workflow when `master` has commits after the latest
GitHub release.

```bash
./release.sh --dry-run
./release.sh
./release.sh --force
```

Crontab (once a day, e.g. 05:00 local time):

```
0 5 * * * /path/to/gallery-ai/release.sh
```

Requires `gh` authenticated with repo + workflow scope. The workflow
`.github/workflows/release.yml` builds PyInstaller binaries (Linux, Windows,
macOS) and publishes them on GitHub. `-U` on those executables uses the `dev`
channel (`CrimsonGlory/gallery-ai`).
