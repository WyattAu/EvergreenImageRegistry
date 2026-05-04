#!/bin/bash
set -euo pipefail

IMAGE="${1:?Usage: bump_versions.sh <image> <new-version>}"
NEW_VERSION="${2:?Usage: bump_versions.sh <image> <new-version>}"

REPO_ROOT="$(git rev-parse --show-toplevel)"
IMAGE_DIR="${REPO_ROOT}/images/${IMAGE}"
DOCKERFILE="${IMAGE_DIR}/Dockerfile"
CHECKSUMS="${IMAGE_DIR}/CHECKSUMS"
MANIFEST="${IMAGE_DIR}/manifest.toml"

if [ ! -d "$IMAGE_DIR" ]; then
    echo "ERROR: Image directory not found: ${IMAGE_DIR}" >&2
    exit 1
fi

if [ ! -f "$DOCKERFILE" ]; then
    echo "ERROR: Dockerfile not found: ${DOCKERFILE}" >&2
    exit 1
fi

OLD_VERSION=""
if grep -qP '^ARG VERSION=' "$DOCKERFILE"; then
    OLD_VERSION=$(grep -oP '^ARG VERSION=\K.*' "$DOCKERFILE" | head -1)
fi

echo "Bumping ${IMAGE}: ${OLD_VERSION} -> ${NEW_VERSION}"

if [ -n "$OLD_VERSION" ]; then
    sed -i "s|^ARG VERSION=.*|ARG VERSION=${NEW_VERSION}|" "$DOCKERFILE"
    sed -i "s|org.opencontainers.image.version=\"${OLD_VERSION}\"|org.opencontainers.image.version=\"${NEW_VERSION}\"|g" "$DOCKERFILE"
    echo "  Updated Dockerfile VERSION and label"
fi

if [ -f "$CHECKSUMS" ]; then
    _OLD_CHECKSUM=$(grep -oP 'expected_sha256\s*=\s*"\K[^"]+' "$CHECKSUMS" 2>/dev/null || echo "")

    DOWNLOAD_URL=$(grep -oP 'url\s*=\s*"\K[^"]+' "$CHECKSUMS" 2>/dev/null | head -1 || echo "")
    if [ -n "$DOWNLOAD_URL" ] && [ -n "$OLD_VERSION" ]; then
        NEW_URL=$(echo "$DOWNLOAD_URL" | sed "s|${OLD_VERSION}|${NEW_VERSION}|g")
        BUMPED_URL=$(echo "$NEW_URL" | sed "s|${OLD_VERSION}|${NEW_VERSION}|g")

        TEMPFILE=$(mktemp)
        HTTP_CODE=$(curl -sS --connect-timeout 10 --max-time 60 -o "$TEMPFILE" -w '%{http_code}' \
            -fsSL "$BUMPED_URL" 2>/dev/null || echo "000")

        if [ "$HTTP_CODE" = "200" ] && [ -s "$TEMPFILE" ]; then
            NEW_CHECKSUM=$(sha256sum "$TEMPFILE" | awk '{print $1}')
            rm -f "$TEMPFILE"

            NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
            sed -i "s|version = \".*\"|version = \"${NEW_VERSION}\"|" "$CHECKSUMS"
            sed -i "s|last_verified = \".*\"|last_verified = \"${NOW}\"|" "$CHECKSUMS"
            sed -i "s|url = \".*\"|url = \"${BUMPED_URL}\"|" "$CHECKSUMS"
            sed -i "s|filename = \".*\"|filename = \"$(basename "$BUMPED_URL")\"|" "$CHECKSUMS"
            sed -i "s|expected_sha256 = \".*\"|expected_sha256 = \"${NEW_CHECKSUM}\"|" "$CHECKSUMS"
            echo "  Updated CHECKSUMS (sha256: ${NEW_CHECKSUM})"
        else
            rm -f "$TEMPFILE"
            NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
            sed -i "s|version = \".*\"|version = \"${NEW_VERSION}\"|" "$CHECKSUMS"
            sed -i "s|expected_sha256 = \".*\"|expected_sha256 = \"NEEDS_UPDATE\"|" "$CHECKSUMS"
            sed -i "s|last_verified = \".*\"|last_verified = \"${NOW}\"|" "$CHECKSUMS"
            echo "  WARNING: Could not download new version to compute checksum (HTTP ${HTTP_CODE})"
            echo "  Set expected_sha256 = \"NEEDS_UPDATE\" in ${CHECKSUMS}"
        fi
    else
        sed -i "s|version = \".*\"|version = \"${NEW_VERSION}\"|" "$CHECKSUMS"
        sed -i "s|expected_sha256 = \".*\"|expected_sha256 = \"NEEDS_UPDATE\"|" "$CHECKSUMS"
        echo "  Updated CHECKSUMS version (checksum marked NEEDS_UPDATE)"
    fi
fi

if [ -f "$MANIFEST" ]; then
    if command -v evergreenctl &>/dev/null; then
        if evergreenctl bump "${IMAGE}" "${NEW_VERSION}" 2>/dev/null; then
            echo "  Updated manifest.toml via evergreenctl"
        else
            echo "  WARNING: evergreenctl bump failed, updating manifest.toml manually"
            sed -i "s|^version = \".*\"|version = \"${NEW_VERSION}\"|g" "$MANIFEST"
            if [ -n "$OLD_VERSION" ]; then
                sed -i "s|${OLD_VERSION}|${NEW_VERSION}|g" "$MANIFEST"
            fi
        fi
    else
        sed -i "s|^version = \".*\"|version = \"${NEW_VERSION}\"|g" "$MANIFEST"
        if [ -n "$OLD_VERSION" ]; then
            sed -i "s|${OLD_VERSION}|${NEW_VERSION}|g" "$MANIFEST"
        fi
        echo "  Updated manifest.toml (evergreenctl not found, used sed)"
    fi
fi

echo "Done: ${IMAGE} bumped from ${OLD_VERSION:-unknown} to ${NEW_VERSION}"
