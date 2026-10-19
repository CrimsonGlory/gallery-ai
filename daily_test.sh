#!/usr/bin/env bash
# Daily unit + live extractor suite: Docker, log results, Grok-fix, commit, push.
#
# Runs scripts/run_tests.py then test/test_results.py in Docker. If anything
# failed, launches one always-approve Grok session. Commits are made by Grok;
# this wrapper pushes when the branch is ahead of origin.
#
# Crontab (once a day). Live suite is ~3h; schedule after release.sh and hold
# the pull_upstream lock so the hourly merge cannot start mid-run:
#   0 2 * * * /path/to/gallery-ai/daily_test.sh
#
# Optional environment:
#   GROK_BIN, GROK_MODEL
#   GALLERY_AI_TEST_IMAGE   Docker image (default: gallery-ai:latest)
#   GALLERY_AI_CONFIG_DIR   gallery-dl config dir mounted into the container
#
# Extra args are forwarded to scripts/daily_test.py
#   ./daily_test.sh --dry-run
#   ./daily_test.sh --no-grok
#   ./daily_test.sh --no-push
#   ./daily_test.sh --from-log tmp/daily-test/live-latest.log
set -euo pipefail

# Cron has a tiny PATH.
export PATH="/usr/local/bin:/usr/bin:/bin:${HOME}/.local/bin:${PATH}"

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
cd "${SCRIPT_DIR}"

LOG_DIR="${SCRIPT_DIR}/tmp/daily-test"
mkdir -p "${LOG_DIR}"

LOCK="${LOG_DIR}/daily_test.lock"
exec 9>"${LOCK}"
if ! flock -n 9; then
    echo "$(date -Iseconds) another daily_test is already running; exiting" >&2
    exit 0
fi

# Hourly pull_upstream.sh uses this lock. Hold it so a merge cannot start
# while the live suite or Grok is rewriting extractors.
UPSTREAM_LOCK_DIR="${SCRIPT_DIR}/tmp/pull-upstream"
mkdir -p "${UPSTREAM_LOCK_DIR}"
exec 8>"${UPSTREAM_LOCK_DIR}/pull_upstream.lock"
if ! flock -w 3600 8; then
    echo "$(date -Iseconds) could not acquire pull_upstream lock; exiting" >&2
    exit 0
fi

STAMP="$(date +%Y-%m-%dT%H%M%S)"
RUN_LOG="${LOG_DIR}/cron-${STAMP}.log"

set +e
{
    echo "=== daily_test ${STAMP} pwd=${SCRIPT_DIR} docker=$(command -v docker) grok=$(command -v grok) ==="
    python3 "${SCRIPT_DIR}/scripts/daily_test.py" \
        --log-dir "${LOG_DIR}" \
        "$@"
} 2>&1 | tee -a "${RUN_LOG}"
rc=${PIPESTATUS[0]}
set -e

# Keep a stable "latest" pointer for tailing.
ln -sfr "${RUN_LOG}" "${LOG_DIR}/cron-latest.log" 2>/dev/null || \
    cp -f "${RUN_LOG}" "${LOG_DIR}/cron-latest.log"

# Drop cron/test/grok logs older than 30 days; keep progress.jsonl.
find "${LOG_DIR}" -maxdepth 1 -type f -name 'cron-*.log' -mtime +30 -delete || true
find "${LOG_DIR}" -maxdepth 1 -type f -name 'unit-*.log' -mtime +30 -delete || true
find "${LOG_DIR}" -maxdepth 1 -type f -name 'live-*.log' -mtime +30 -delete || true
find "${LOG_DIR}" -maxdepth 1 -type f -name 'prompt-*.txt' -mtime +30 -delete || true
find "${LOG_DIR}" -maxdepth 1 -type f -name 'summary-*.json' -mtime +30 -delete || true
find "${LOG_DIR}/grok" -maxdepth 1 -type f -name '*.log' -mtime +30 -delete 2>/dev/null || true

exit "${rc}"
