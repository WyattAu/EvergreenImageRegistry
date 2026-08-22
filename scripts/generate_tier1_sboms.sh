#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry - Tier 1 SBOM Generator
# =============================================================================
# Generates SPDX 2.3 SBOMs for all Tier 1 (critical) images.
# Uses Syft to scan images and produces repo-committable SBOM files.
#
# Usage:
#   ./scripts/generate_tier1_sboms.sh [OPTIONS]
#
# Options:
#   --dry-run       Show what would be generated without writing
#   --image <name>  Generate SBOM for a specific image only
#   --commit        Auto-commit generated SBOMs
#   --help          Show this help
#
# Prerequisites:
#   - syft (https://github.com/anchore/syft)
#   - docker (for pulling images)
#   - ghcr.io access (for pulling from GHCR)
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

DRY_RUN=false
TARGET_IMAGE=""
AUTO_COMMIT=false
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
REGISTRY="ghcr.io/wyattau/evergreenimageregistry"

usage() {
    head -20 "$0" | tail -18
    exit 0
}

log_info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ---- Parse arguments ----
while [ $# -gt 0 ]; do
    case "$1" in
        --dry-run)   DRY_RUN=true; shift ;;
        --image)     TARGET_IMAGE="$2"; shift 2 ;;
        --commit)    AUTO_COMMIT=true; shift ;;
        --help)      usage ;;
        *)           log_error "Unknown option: $1"; usage ;;
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
    log_error "Docker not found. Cannot pull images."
    exit 1
fi

# ---- Find Tier 1 images ----
find_tier1_images() {
    local images=()
    for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
        [ -f "$manifest" ] || continue
        local tier
        tier=$(grep -oP 'tier\s*=\s*"\K[^"]+' "$manifest" 2>/dev/null || echo "standard")
        if [ "$tier" = "critical" ]; then
            local img_name
            img_name=$(basename "$(dirname "$manifest")")
            images+=("$img_name")
        fi
    done
    echo "${images[@]}"
}

# ---- Check if SBOM already exists and is recent ----
sbom_exists_and_fresh() {
    local img="$1"
    local sbom_path="$REPO_ROOT/images/$img/sbom.spdx.json"
    
    if [ ! -f "$sbom_path" ]; then
        return 1  # Does not exist
    fi
    
    # Check if file has content (not just a template)
    local size
    size=$(stat --format=%s "$sbom_path" 2>/dev/null || stat -f%z "$sbom_path" 2>/dev/null || echo "0")
    if [ "$size" -lt 1000 ]; then
        return 1  # Too small, likely a template
    fi
    
    # Check if it has actual packages
    local pkg_count
    pkg_count=$(python3 -c "
import json
try:
    with open('$sbom_path') as f:
        data = json.load(f)
    print(len(data.get('packages', [])))
except:
    print(0)
" 2>/dev/null || echo "0")
    
    if [ "$pkg_count" -gt 0 ]; then
        return 0  # Exists and has packages
    fi
    
    return 1  # Exists but is empty/template
}

# ---- Generate SBOM for a single image ----
generate_sbom() {
    local img="$1"
    local sbom_path="$REPO_ROOT/images/$img/sbom.spdx.json"
    local ref="${REGISTRY}/${img}:latest"
    
    log_info "Generating SBOM for ${img}..."
    
    # Check if already exists
    if sbom_exists_and_fresh "$img"; then
        local pkg_count
        pkg_count=$(python3 -c "
import json
with open('$sbom_path') as f:
    data = json.load(f)
print(len(data.get('packages', [])))
" 2>/dev/null || echo "0")
        log_ok "SBOM already exists (${pkg_count} packages): ${img}"
        return 0
    fi
    
    # Pull the image
    if ! docker manifest inspect "$ref" >/dev/null 2>&1; then
        log_warn "Image not found in registry: ${ref}"
        return 1
    fi
    
    if [ "$DRY_RUN" = true ]; then
        log_info "Would generate: ${sbom_path}"
        return 0
    fi
    
    # Pull image locally
    if ! docker image inspect "$ref" >/dev/null 2>&1; then
        log_info "Pulling ${ref}..."
        docker pull "$ref" 2>/dev/null || {
            log_warn "Failed to pull ${ref}"
            return 1
        }
    fi
    
    # Generate SPDX SBOM
    if syft scan "$ref" -o spdx-json > "$sbom_path" 2>/dev/null; then
        local pkg_count
        pkg_count=$(python3 -c "
import json
with open('$sbom_path') as f:
    data = json.load(f)
print(len(data.get('packages', [])))
" 2>/dev/null || echo "?")
        log_ok "Generated SBOM for ${img} (${pkg_count} packages)"
        
        # Clean up local image
        docker rmi "$ref" 2>/dev/null || true
        return 0
    else
        log_error "Failed to generate SBOM for ${img}"
        rm -f "$sbom_path"
        return 1
    fi
}

# ---- Main ----
log_info "Tier 1 SBOM Generator"
log_info "====================="
echo ""

if [ -n "$TARGET_IMAGE" ]; then
    # Single image mode
    generate_sbom "$TARGET_IMAGE"
else
    # Batch mode — find Tier 1 images directly (avoids array truncation)
    images=()
    for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
        [ -f "$manifest" ] || continue
        tier=$(grep -oP 'tier\s*=\s*"\K[^"]+' "$manifest" 2>/dev/null | head -1)
        if [ "$tier" = "critical" ]; then
            images+=("$(basename "$(dirname "$manifest")")")
        fi
    done
    total=${#images[@]}
    log_info "Found ${total} Tier 1 images"
    echo ""
    
    generated=0
    skipped=0
    failed=0
    
    for img in "${images[@]}"; do
        if generate_sbom "$img"; then
            if sbom_exists_and_fresh "$img"; then
                skipped=$((skipped + 1))
            else
                generated=$((generated + 1))
            fi
        else
            failed=$((failed + 1))
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

Generated SBOMs using Syft for all Tier 1 (critical) images.
Each SBOM contains package inventory, dependencies, and licensing.

🤖 Generated with Codebuff
Co-Authored-By: Codebuff <noreply@codebuff.com>
EOF
        )" || log_warn "Nothing to commit"
    fi
fi
