#!/usr/bin/env bash
# Dispatch GitHub Actions "Release" only when master has commits after the
# last GitHub release. gallery-ai has a single release channel (no nightly/stable).
#
# Uses the GitHub API only (no local git history required).
#
# Crontab (once a day, e.g. 05:00 local time):
#   0 5 * * * /path/to/gallery-ai/release.sh
#
# Requires: gh authenticated with repo + workflow scope for GALLERY_AI_REPO.
#
# Optional environment:
#   GALLERY_AI_REPO      default CrimsonGlory/gallery-ai
#   GALLERY_AI_BRANCH    default master
#   GALLERY_AI_WORKFLOW  default Release
#
# Extra args:
#   ./release.sh --dry-run
#   ./release.sh --force
set -euo pipefail

# Cron has a tiny PATH.
export PATH="/usr/local/bin:/usr/bin:/bin:${HOME}/.local/bin:${PATH}"

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
cd "${SCRIPT_DIR}"

REPO="${GALLERY_AI_REPO:-CrimsonGlory/gallery-ai}"
BRANCH="${GALLERY_AI_BRANCH:-master}"
WORKFLOW="${GALLERY_AI_WORKFLOW:-Release}"

DRY_RUN=0
FORCE=0
for arg in "$@"; do
    case "${arg}" in
        --dry-run) DRY_RUN=1 ;;
        --force) FORCE=1 ;;
        -h|--help)
            sed -n '2,19p' "$0"
            exit 0
            ;;
        *)
            echo "Unknown argument: ${arg}" >&2
            echo "Usage: $0 [--dry-run] [--force]" >&2
            exit 2
            ;;
    esac
done

LOG_DIR="${SCRIPT_DIR}/tmp/release"
mkdir -p "${LOG_DIR}"

LOCK="${LOG_DIR}/release.lock"
exec 9>"${LOCK}"
if ! flock -n 9; then
    echo "$(date -Iseconds) another release.sh is already running; exiting" >&2
    exit 0
fi

STAMP="$(date +%Y-%m-%dT%H%M%S)"
RUN_LOG="${LOG_DIR}/cron-${STAMP}.log"

log() {
    echo "$(date -Iseconds) $*"
}

active_release_runs() {
    gh run list \
        --repo "${REPO}" \
        --workflow "${WORKFLOW}" \
        --limit 20 \
        --json status \
        --jq '[.[] | select(.status == "queued" or .status == "in_progress" or .status == "waiting" or .status == "pending" or .status == "requested")] | length'
}

latest_release_tag() {
    local tag
    # GitHub's "latest" is the newest non-prerelease, non-draft release.
    tag="$(gh api "repos/${REPO}/releases/latest" --jq '.tag_name' 2>/dev/null || true)"
    if [[ -n "${tag}" && "${tag}" != "null" ]]; then
        printf '%s' "${tag}"
        return 0
    fi
    gh release list \
        --repo "${REPO}" \
        --exclude-drafts \
        --limit 1 \
        --json tagName \
        --jq '.[0].tagName // empty'
}

commits_ahead() {
    local tag="$1"
    gh api "repos/${REPO}/compare/${tag}...${BRANCH}" --jq '.ahead_by'
}

trigger_release() {
    if ((DRY_RUN)); then
        log "dry-run: would run: gh workflow run ${WORKFLOW} --repo ${REPO} --ref ${BRANCH}"
        return 0
    fi
    gh workflow run "${WORKFLOW}" --repo "${REPO}" --ref "${BRANCH}"
    log "dispatched ${WORKFLOW} on ${REPO}@${BRANCH}"
}

set +e
{
    set -euo pipefail
    log "=== release.sh ${STAMP} repo=${REPO} branch=${BRANCH} ==="

    if ! command -v gh >/dev/null 2>&1; then
        log "error: gh is not installed or not on PATH"
        exit 1
    fi

    if ! gh auth status --hostname github.com >/dev/null 2>&1; then
        log "error: gh is not authenticated for github.com"
        exit 1
    fi

    if ! gh workflow view "${WORKFLOW}" --repo "${REPO}" >/dev/null 2>&1; then
        log "error: workflow '${WORKFLOW}' not found on ${REPO}"
        log "push .github/workflows/release.yml to ${BRANCH} first"
        exit 1
    fi

    active="$(active_release_runs)"
    if [[ "${active}" -gt 0 ]]; then
        log "${WORKFLOW} already has ${active} active run(s); skipping"
        exit 0
    fi

    if ((FORCE)); then
        log "--force: skipping commit check"
        trigger_release
        exit 0
    fi

    last_tag="$(latest_release_tag)"
    if [[ -z "${last_tag}" ]]; then
        log "no GitHub releases found; treating as new work"
        trigger_release
        exit 0
    fi

    ahead="$(commits_ahead "${last_tag}")"
    if [[ "${ahead}" -gt 0 ]]; then
        log "${ahead} commit(s) on ${BRANCH} since ${last_tag}; triggering ${WORKFLOW}"
        trigger_release
    else
        log "no new commits on ${BRANCH} since ${last_tag}; skipping"
    fi
} 2>&1 | tee -a "${RUN_LOG}"
rc=${PIPESTATUS[0]}
set -e

ln -sfr "${RUN_LOG}" "${LOG_DIR}/cron-latest.log" 2>/dev/null || \
    cp -f "${RUN_LOG}" "${LOG_DIR}/cron-latest.log"

find "${LOG_DIR}" -maxdepth 1 -type f -name 'cron-*.log' -mtime +30 -delete || true

exit "${rc}"
