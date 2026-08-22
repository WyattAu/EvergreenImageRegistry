#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry — Offline SBOM Generator
# =============================================================================
# Pre-generates SBOMs for air-gapped environments where registry access
# is not available. Builds images locally and generates SBOMs.
#
# Usage:
#   ./scripts/generate_offline_sboms.sh --tier1
#   ./scripts/generate_offline_sboms.sh --image redis
#   ./scripts/generate_offline_sboms.sh --all --output /opt/offline-sboms/
# =============================================================================

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
NC='\033[0m'

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OUTPUT_DIR="$REPO_ROOT/compliance/offline-sboms"
TARGET_IMAGE=""
TIER1_ONLY=false
ALL_MODE=false

log_info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

while [ $# -gt 0 ]; do
    case "$1" in
        --image)    TARGET_IMAGE="$2"; shift 2 ;;
        --tier1)    TIER1_ONLY=true; shift ;;
        --all)      ALL_MODE=true; shift ;;
        --output)   OUTPUT_DIR="$2"; shift 2 ;;
        --help)     head -22 "$0" | tail -20; exit 0 ;;
        *)          log_error "Unknown: $1"; exit 1 ;;
    esac
done

mkdir -p "$OUTPUT_DIR"

# Check prerequisites
if ! command -v syft &>/dev/null; then
    log_error "Syft not found. Install: curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin"
    exit 1
fi

# ---- Build and scan offline ----
offline_scan() {
    local img="$1"
    local dockerfile="$REPO_ROOT/images/$img/Dockerfile"
    local sbom_path="$OUTPUT_DIR/${img}.sbom.spdx.json"

    [ -f "$dockerfile" ] || return 1

    log_info "Building $img for offline SBOM..."

    local tag="evergreen-offline:${img}"

    # Build locally
    if ! docker build -t "$tag" -f "$dockerfile" "$REPO_ROOT/images/$img/" >/dev/null 2>&1; then
        log_error "Build failed: $img"
        return 1
    fi

    # Generate SBOM from local image
    if syft scan "$tag" -o spdx-json > "$sbom_path" 2>/dev/null; then
        local pkg_count
        pkg_count=$(python3 -c "import json; print(len(json.load(open('$sbom_path')).get('packages',[])))" 2>/dev/null || echo "?")
        log_ok "SBOM generated: $img ($pkg_count packages)"
        docker rmi "$tag" 2>/dev/null || true
        return 0
    else
        log_error "Syft failed: $img"
        rm -f "$sbom_path"
        docker rmi "$tag" 2>/dev/null || true
        return 1
    fi
}

# ---- Main ----
log_info "Offline SBOM Generator"
log_info "======================"
echo ""

if [ -n "$TARGET_IMAGE" ]; then
    offline_scan "$TARGET_IMAGE"
else
    images=()
    if [ "$ALL_MODE" = true ]; then
        for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
            images+=("$(basename "$(dirname "$manifest")")")
        done
    else
        for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
            tier=$(grep -oP 'tier\s*=\s*"\K[^"]+' "$manifest" 2>/dev/null | head -1)
            [ "$tier" = "critical" ] && images+=("$(basename "$(dirname "$manifest")")")
        done
    fi

    total=${#images[@]}
    log_info "Building $total images for offline SBOMs"
    echo ""

    generated=0
    failed=0
    for img in "${images[@]}"; do
        if offline_scan "$img"; then
            generated=$((generated + 1))
        else
            failed=$((failed + 1))
        fi
    done

    echo ""
    echo "=========================================="
    echo "Offline SBOM Generation Complete"
    echo "=========================================="
    echo "  Generated: $generated"
    echo "  Failed:    $failed"
    echo "  Output:    $OUTPUT_DIR/"
    echo ""
    echo "For air-gapped environments:"
    echo "  cp -r $OUTPUT_DIR /opt/offline-sboms/"
    echo "  syft scan <image> -o spdx-json=<output>  # requires local image"
    echo "=========================================="
fi
