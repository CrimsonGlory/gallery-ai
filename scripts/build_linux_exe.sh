#!/usr/bin/env bash
# Build gallery-ai_linux with PyInstaller against glibc 2.17 (manylinux2014).
# The GitHub-hosted ubuntu-latest Python 3.14 is linked to GLIBC_2.38+, which
# will not run on Debian 12 (glibc 2.36). This image matches yt-ai_linux.
set -euo pipefail

ROOT="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "${ROOT}"

IMAGE="${GALLERY_AI_LINUX_IMAGE:-ghcr.io/yt-dlp/manylinux2014_x86_64-shared@sha256:4faf3be022c04a457f9176ede4d086f0a8f5794cc6dc267bcb16ad6b903ec294}"
VERIFY_IMAGE="${GALLERY_AI_LINUX_VERIFY_IMAGE:-debian:bookworm-slim}"

inside() {
    PY="${GALLERY_AI_LINUX_PYTHON:-/opt/shared-cpython-3.14/bin/python3.14}"
    if [[ ! -x "${PY}" ]]; then
        echo "shared CPython not found: ${PY}" >&2
        exit 1
    fi
    "${PY}" -m venv /tmp/gdl-venv
    # shellcheck disable=SC1091
    source /tmp/gdl-venv/bin/activate
    python -m pip install --no-input --disable-pip-version-check \
        --require-hashes -r requirements/pip
    python -m pip install --no-input --disable-pip-version-check \
        --require-hashes -r requirements/linux
    python ./scripts/pyinstaller.py --label linux
    chmod +x dist/gallery-ai_linux
}

if [[ "${1:-}" == "--inside" ]]; then
    inside
    exit 0
fi

mkdir -p dist build

docker run --rm \
    --user "$(id -u):$(id -g)" \
    -e HOME=/tmp \
    -e XDG_CACHE_HOME=/tmp/cache \
    -v "${ROOT}:/src" \
    -w /src \
    "${IMAGE}" \
    bash /src/scripts/build_linux_exe.sh --inside

chmod +x dist/gallery-ai_linux

echo "Built dist/gallery-ai_linux"
file dist/gallery-ai_linux || true
ldd dist/gallery-ai_linux || true

echo "Verifying on ${VERIFY_IMAGE} (Debian 12 / glibc 2.36)"
docker run --rm \
    -v "${ROOT}/dist:/dist:ro" \
    "${VERIFY_IMAGE}" \
    /dist/gallery-ai_linux --version
