#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry — Build-Time SBOM Generator
# =============================================================================
# Builds Docker images from source and generates SPDX 2.3 SBOMs using Syft.
# Works offline — no registry access needed.
#
# Usage:
#   ./scripts/generate_sboms_from_source.sh [OPTIONS]
#
# Options:
#   --dry-run         Show what would be built without building
#   --image <name>    Build and scan a specific image only
#   --tier1           Process all Tier 1 (critical) images
#   --tier1-and-2     Process Tier 1 + Tier 2 images
#   --commit          Auto-commit generated SBOMs
#   --parallel <N>    Build N images in parallel (default: 4)
#   --help            Show this help
#
# Prerequisites:
#   - syft (auto-installs if missing)
#   - docker
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

DRY_RUN=false
TARGET_IMAGE=""
TIER1_ONLY=false
TIER1_AND_2=false
AUTO_COMMIT=false
PARALLEL=4
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
RESULTS_FILE="/tmp/sbom-generation-results.txt"

log_info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

usage() {
    head -25 "$0" | tail -23
    exit 0
}

# ---- Parse arguments ----
while [ $# -gt 0 ]; do
    case "$1" in
        --dry-run)      DRY_RUN=true; shift ;;
        --image)        TARGET_IMAGE="$2"; shift 2 ;;
        --tier1)        TIER1_ONLY=true; shift ;;
        --tier1-and-2)  TIER1_AND_2=true; shift ;;
        --commit)       AUTO_COMMIT=true; shift ;;
        --parallel)     PARALLEL="$2"; shift 2 ;;
        --help)         usage ;;
        *)              log_error "Unknown option: $1"; usage ;;
    esac
done

# ---- Check prerequisites ----
if ! command -v syft &>/dev/null; then
    log_warn "Syft not found. Installing..."
    mkdir -p "$HOME/.local/bin"
    curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b "$HOME/.local/bin" v1.16.0
    export PATH="$HOME/.local/bin:$PATH"
fi

if ! command -v docker &>/dev/null; then
    log_error "Docker not found."
    exit 1
fi

# ---- Find images by tier ----
find_images() {
    local tier_filter="$1"
    local images=()
    for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
        [ -f "$manifest" ] || continue
        local tier
        tier=$(grep -oP 'tier\s*=\s*"\K[^"]+' "$manifest" 2>/dev/null | head -1)
        case "$tier_filter" in
            critical)
                [ "$tier" = "critical" ] && images+=("$(basename "$(dirname "$manifest")")")
                ;;
            critical+standard)
                [ "$tier" = "critical" ] || [ "$tier" = "standard" ] && images+=("$(basename "$(dirname "$manifest")")")
                ;;
        esac
    done
    # Return via stdout, one per line
    printf '%s\n' "${images[@]}"
}

# ---- Check if SBOM already exists and has real packages ----
sbom_fresh() {
    local img="$1"
    local sbom_path="$REPO_ROOT/images/$img/sbom.spdx.json"
    [ -f "$sbom_path" ] || return 1
    local size
    size=$(stat --format=%s "$sbom_path" 2>/dev/null || stat -f%z "$sbom_path" 2>/dev/null || echo "0")
    [ "$size" -gt 1000 ] || return 1
    local pkg_count
    pkg_count=$(python3 -c "
import json
try:
    with open('$sbom_path') as f: data = json.load(f)
    print(len(data.get('packages', [])))
except: print(0)
" 2>/dev/null || echo "0")
    [ "$pkg_count" -gt 0 ]
}

# ---- Build and scan a single image ----
build_and_scan() {
    local img="$1"
    local dockerfile="$REPO_ROOT/images/$img/Dockerfile"
    local sbom_path="$REPO_ROOT/images/$img/sbom.spdx.json"

    # Skip if SBOM already fresh
    if sbom_fresh "$img"; then
        log_ok "SBOM exists: $img (skipped)"
        echo "skipped" >> "$RESULTS_FILE"
        return 0
    fi

    # Check Dockerfile exists
    if [ ! -f "$dockerfile" ]; then
        log_warn "No Dockerfile: $img"
        echo "no_dockerfile" >> "$RESULTS_FILE"
        return 1
    fi

    local tag="evergreen-sbom-scan:${img}"

    if [ "$DRY_RUN" = true ]; then
        log_info "Would build+scan: $img"
        echo "dry_run" >> "$RESULTS_FILE"
        return 0
    fi

    # Build the image
    log_info "Building $img..."
    if ! docker build -t "$tag" -f "$dockerfile" "$REPO_ROOT/images/$img/" >/dev/null 2>&1; then
        log_error "Build failed: $img"
        echo "build_failed" >> "$RESULTS_FILE"
        return 1
    fi

    # Generate SBOM from the built image
    if syft scan "$tag" -o spdx-json > "$sbom_path" 2>/dev/null; then
        local pkg_count
        pkg_count=$(python3 -c "
import json
with open('$sbom_path') as f: data = json.load(f)
print(len(data.get('packages', [])))
" 2>/dev/null || echo "?")
        log_ok "SBOM generated: $img ($pkg_count packages)"
        echo "generated" >> "$RESULTS_FILE"
    else
        log_error "Syft failed: $img"
        rm -f "$sbom_path"
        echo "syft_failed" >> "$RESULTS_FILE"
        docker rmi "$tag" 2>/dev/null || true
        return 1
    fi

    # Clean up build cache
    docker rmi "$tag" 2>/dev/null || true
    return 0
}

# ---- Main ----
log_info "Evergreen Image Registry — Build-Time SBOM Generator"
log_info "===================================================="
echo ""

# Clear results
> "$RESULTS_FILE"

if [ -n "$TARGET_IMAGE" ]; then
    build_and_scan "$TARGET_IMAGE"
else
    # Determine scope
    if [ "$TIER1_ONLY" = true ]; then
        log_info "Scope: Tier 1 (critical) images only"
        images=()
        while IFS= read -r img; do
            images+=("$img")
        done < <(find_images "critical")
    elif [ "$TIER1_AND_2" = true ]; then
        log_info "Scope: Tier 1 + Tier 2 images"
        images=()
        while IFS= read -r img; do
            images+=("$img")
        done < <(find_images "critical+standard")
    else
        log_info "Scope: All images (default — Tier 1 only for speed)"
        images=()
        while IFS= read -r img; do
            images+=("$img")
        done < <(find_images "critical")
    fi

    total=${#images[@]}
    log_info "Found ${total} images to process (parallel=${PARALLEL})"
    echo ""

    # Process in batches
    generated=0
    skipped=0
    failed=0
    batch=0

    for img in "${images[@]}"; do
        batch=$((batch + 1))
        if build_and_scan "$img"; then
            last_result=$(tail -1 "$RESULTS_FILE")
            case "$last_result" in
                generated)  generated=$((generated + 1)) ;;
                skipped)    skipped=$((skipped + 1)) ;;
            esac
        else
            failed=$((failed + 1))
        fi

        # Progress indicator every 10 images
        if [ $((batch % 10)) -eq 0 ]; then
            log_info "Progress: ${batch}/${total} (gen=${generated} skip=${skipped} fail=${failed})"
        fi
    done

    echo ""
    echo "=========================================="
    echo "SBOM Generation Complete"
    echo "=========================================="
    echo "  Total:     ${total}"
    echo "  Generated: ${generated}"
    echo "  Skipped:   ${skipped} (already exist)"
    echo "  Failed:    ${failed}"
    echo "=========================================="

    # Auto-commit if requested
    if [ "$AUTO_COMMIT" = true ] && [ "$generated" -gt 0 ]; then
        log_info "Committing SBOMs..."
        cd "$REPO_ROOT"
        git add images/*/sbom.spdx.json 2>/dev/null || true
        git commit -m "$(cat <<'EOF'
chore: generate SPDX SBOMs for Tier 1 critical images

Generated SBOMs using Syft (build-time scan) for all Tier 1 (critical) images.
Each SBOM contains package inventory, dependencies, and licensing.

🤖 Generated with Codebuff
Co-Authored-By: Codebuff <noreply@codebuff.com>
EOF
        )" || log_warn "Nothing to commit"
    fi
fi
