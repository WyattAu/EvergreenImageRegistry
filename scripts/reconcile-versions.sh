#!/bin/bash
# =============================================================================
# manifest.toml Version Reconciliation Script
# =============================================================================
# Compares version information across three sources:
#   1. Dockerfile ARG VERSION (what gets built)
#   2. manifest.toml metadata.version (what CI pushes as tag)
#   3. manifest.toml upstream_version (latest upstream)
#
# Reports mismatches and optionally fixes them.
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
IMAGES_DIR="${REPO_ROOT}/images"

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

DRY_RUN=${DRY_RUN:-false}
FIX_ALL=${FIX_ALL:-false}

echo "=== EIR Manifest.toml Version Reconciliation ==="
echo "Mode: $(if $DRY_RUN; then echo 'DRY RUN'; else echo 'LIVE'; fi)"
echo ""

DRIFT_COUNT=0
FIXED_COUNT=0

for image_dir in "${IMAGES_DIR}"/*/; do
    image=$(basename "$image_dir")
    [ ! -f "${image_dir}/Dockerfile" ] && continue
    [ ! -f "${image_dir}/manifest.toml" ] && continue

    # Extract versions from each source
    dockerfile_ver=$(grep -oP '(?<=^ARG VERSION=).*' "${image_dir}/Dockerfile" 2>/dev/null | head -1)
    manifest_ver=$(grep -oP '^version\s*=\s*"\K[^"]+' "${image_dir}/manifest.toml" 2>/dev/null | head -1)
    upstream_ver=$(grep -oP 'upstream_version\s*=\s*"\K[^"]+' "${image_dir}/manifest.toml" 2>/dev/null | head -1)

    # Check for mismatches
    issues=()

    if [ -n "$dockerfile_ver" ] && [ -n "$manifest_ver" ] && [ "$dockerfile_ver" != "$manifest_ver" ]; then
        issues+=("Dockerfile($dockerfile_ver) != manifest($manifest_ver)")
    fi

    if [ -n "$dockerfile_ver" ] && [ -n "$upstream_ver" ] && [ "$dockerfile_ver" != "$upstream_ver" ]; then
        issues+=("Dockerfile($dockerfile_ver) != upstream($upstream_ver)")
    fi

    if [ -n "$manifest_ver" ] && [ -n "$upstream_ver" ] && [ "$manifest_ver" != "$upstream_ver" ]; then
        issues+=("manifest($manifest_ver) != upstream($upstream_ver)")
    fi

    if [ ${#issues[@]} -gt 0 ]; then
        DRIFT_COUNT=$((DRIFT_COUNT + 1))
        echo -e "${RED}DRIFT${NC}: ${image}"
        for issue in "${issues[@]}"; do
            echo "  - $issue"
        done

        if $FIX_ALL && [ -n "$dockerfile_ver" ] && [ "$dockerfile_ver" != "latest" ]; then
            echo -e "  ${YELLOW}FIX: Updating manifest.toml version to ${dockerfile_ver}${NC}"
            if ! $DRY_RUN; then
                sudo sed -i "s/^version = .*/version = \"${dockerfile_ver}\"/" "${image_dir}/manifest.toml"
                FIXED_COUNT=$((FIXED_COUNT + 1))
            fi
        fi
        echo ""
    fi
done

echo "=== Summary ==="
echo "Total images checked: $(ls -d "${IMAGES_DIR}"/*/ | wc -l)"
echo "Images with drift: ${DRIFT_COUNT}"
if $FIX_ALL; then
    echo "Images fixed: ${FIXED_COUNT}"
fi

if [ $DRIFT_COUNT -eq 0 ]; then
    echo -e "${GREEN}All versions are in sync!${NC}"
fi
