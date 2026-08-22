#!/usr/bin/env bash
# =============================================================================
# Batch SBOM Generator — Handles timeouts and retries
# =============================================================================
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
REGISTRY="ghcr.io/wyattau/evergreenimageregistry"
TIMEOUT=180  # 3 minutes per image

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log_ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_err()  { echo -e "${RED}[FAIL]${NC} $1"; }

build_and_scan() {
    local img="$1"
    local dockerfile="$REPO_ROOT/images/$img/Dockerfile"
    local sbom_path="$REPO_ROOT/images/$img/sbom.spdx.json"

    # Skip if SBOM already exists with packages
    if [ -f "$sbom_path" ]; then
        local size=$(stat --format=%s "$sbom_path" 2>/dev/null || echo 0)
        if [ "$size" -gt 1000 ]; then
            return 0  # Already done
        fi
    fi

    [ -f "$dockerfile" ] || return 1

    local tag="evergreen-sbom:${img}"

    # Build with timeout
    if ! timeout $TIMEOUT docker build -t "$tag" -f "$dockerfile" "$REPO_ROOT/images/$img/" >/dev/null 2>&1; then
        log_err "Build failed/timeout: $img"
        return 1
    fi

    # Generate SBOM
    if syft scan "$tag" -o spdx-json > "$sbom_path" 2>/dev/null; then
        local pkg_count=$(python3 -c "import json; print(len(json.load(open('$sbom_path')).get('packages',[])))" 2>/dev/null || echo "?")
        log_ok "$img ($pkg_count packages)"
        docker rmi "$tag" 2>/dev/null || true
        return 0
    else
        log_err "Syft failed: $img"
        rm -f "$sbom_path"
        docker rmi "$tag" 2>/dev/null || true
        return 1
    fi
}

# Find images without SBOMs
images=()
for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
    [ -f "$manifest" ] || continue
    img=$(basename "$(dirname "$manifest")")
    sbom="$REPO_ROOT/images/$img/sbom.spdx.json"
    if [ ! -f "$sbom" ] || [ "$(stat --format=%s "$sbom" 2>/dev/null || echo 0)" -lt 1000 ]; then
        images+=("$img")
    fi
done

echo "Found ${#images[@]} images without SBOMs"
echo ""

generated=0
failed=0

for img in "${images[@]}"; do
    if build_and_scan "$img"; then
        generated=$((generated + 1))
    else
        failed=$((failed + 1))
    fi
done

echo ""
echo "=========================================="
echo "Generated: $generated | Failed: $failed"
echo "=========================================="
