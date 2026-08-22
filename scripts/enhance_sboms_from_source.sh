#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry — SBOM Enhancement from Source
# =============================================================================
# Enhances existing SBOMs by extracting source URLs from Dockerfiles,
# downloading source archives, scanning with syft, and merging results.
#
# Usage:
#   ./scripts/enhance_sboms_from_source.sh [OPTIONS]
#
# Options:
#   --image <name>    Enhance SBOM for a specific image only
#   --tier1           Process all Tier 1 (critical) images only
#   --dry-run         Show what would be processed without doing it
#   --parallel <N>    Process N images in parallel (default: 2)
#   --help            Show this help
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
PARALLEL=2
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
RESULTS_FILE="/tmp/sbom-enhancement-results.txt"
TEMP_DIR=$(mktemp -d)

trap 'rm -rf "$TEMP_DIR"' EXIT

log_info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --image) TARGET_IMAGE="$2"; shift 2 ;;
        --tier1) TIER1_ONLY=true; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        --parallel) PARALLEL="$2"; shift 2 ;;
        --help) head -20 "$0" | tail -18; exit 0 ;;
        *) log_error "Unknown option: $1"; exit 1 ;;
    esac
done

# Check prerequisites
if ! command -v syft &>/dev/null; then
    log_error "syft not found. Install: curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin"
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    log_error "python3 not found"
    exit 1
fi

# Extract source URL from Dockerfile
extract_source_url() {
    local dockerfile="$1"
    # Look for wget/curl commands that download source archives
    grep -oP '(wget|curl)\s+[^"]*https?://[^"]+\.(tar\.gz|tar\.bz2|tar\.xz|zip|tgz)' "$dockerfile" 2>/dev/null | \
        grep -oP 'https?://[^"]+' | head -1 || true
}

# Extract version from Dockerfile ARG
extract_version() {
    local dockerfile="$1"
    grep -oP 'ARG\s+VERSION=\K[^ ]+' "$dockerfile" 2>/dev/null | head -1 || true
}

# Generate enhanced SBOM for a single image
enhance_sbom() {
    local img_name="$1"
    local img_dir="$REPO_ROOT/images/$img_name"
    local dockerfile="$img_dir/Dockerfile"
    local existing_sbom="$img_dir/sbom.spdx.json"

    if [[ ! -f "$dockerfile" ]]; then
        return 1
    fi

    # Check if image is scratch-based (these benefit most from enhancement)
    local last_from
    last_from=$(grep '^FROM ' "$dockerfile" | tail -1)
    if ! echo "$last_from" | grep -q 'scratch'; then
        # Not scratch-based, skip (upstream repacks already have good SBOMs)
        return 0
    fi

    # Extract source URL
    local source_url
    source_url=$(extract_source_url "$dockerfile")

    if [[ -z "$source_url" ]]; then
        return 0
    fi

    # Extract version
    local version
    version=$(extract_version "$dockerfile")

    # Download source archive
    local archive_name=$(basename "$source_url")
    local archive_path="$TEMP_DIR/$img_name/$archive_name"
    mkdir -p "$TEMP_DIR/$img_name"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would enhance SBOM for $img_name from $source_url"
        return 0
    fi

    log_info "Downloading source for $img_name: $source_url"
    if ! curl -sSfL "$source_url" -o "$archive_path" 2>/dev/null; then
        log_warn "Failed to download source for $img_name"
        return 1
    fi

    # Extract source
    local source_dir="$TEMP_DIR/$img_name/src"
    mkdir -p "$source_dir"
    if [[ "$archive_name" == *.tar.gz ]] || [[ "$archive_name" == *.tgz ]]; then
        tar -xzf "$archive_path" -C "$source_dir" 2>/dev/null || true
    elif [[ "$archive_name" == *.tar.bz2 ]]; then
        tar -xjf "$archive_path" -C "$source_dir" 2>/dev/null || true
    elif [[ "$archive_name" == *.tar.xz ]]; then
        tar -xJf "$archive_path" -C "$source_dir" 2>/dev/null || true
    elif [[ "$archive_name" == *.zip ]]; then
        unzip -q "$archive_path" -d "$source_dir" 2>/dev/null || true
    fi

    # Scan source with syft
    local source_sbom="$TEMP_DIR/$img_name/source-sbom.json"
    if syft dir:"$source_dir" -o spdx-json="$source_sbom" 2>/dev/null; then
        local source_packages
        source_packages=$(python3 -c "import json; print(len(json.load(open('$source_sbom')).get('packages', [])))" 2>/dev/null || echo 0)

        if [[ "$source_packages" -gt 0 ]]; then
            # Merge source packages into existing SBOM
            python3 -c "
import json, sys

# Load existing SBOM
try:
    existing = json.load(open('$existing_sbom'))
except:
    existing = {'spdxVersion': 'SPDX-2.3', 'name': '$img_name', 'packages': []}

# Load source SBOM
source = json.load(open('$source_sbom'))

# Merge packages (deduplicate by name+version)
existing_names = {(p.get('name', ''), p.get('version', '')) for p in existing.get('packages', [])}
added = 0
for pkg in source.get('packages', []):
    key = (pkg.get('name', ''), pkg.get('version', ''))
    if key not in existing_names and pkg.get('name', '') != '$img_name':
        # Add source reference
        pkg['supplier'] = 'NOASSERTION'
        if 'downloadLocation' not in pkg or pkg['downloadLocation'] == 'NOASSERTION':
            pkg['downloadLocation'] = '$source_url'
        existing.setdefault('packages', []).append(pkg)
        existing_names.add(key)
        added += 1

# Write enhanced SBOM
with open('$existing_sbom', 'w') as f:
    json.dump(existing, f, indent=2)

print(f'Added {added} source packages')
" 2>/dev/null && log_ok "Enhanced $img_name SBOM" && return 0
        fi
    fi

    return 1
}

# Get list of images to process
get_images() {
    local images=()
    for img_dir in "$REPO_ROOT"/images/*/; do
        local name
        name=$(basename "$img_dir")

        # Skip excluded directories
        [[ "$name" == _* ]] && continue

        # Filter by target image
        if [[ -n "$TARGET_IMAGE" && "$name" != "$TARGET_IMAGE" ]]; then
            continue
        fi

        # Filter by tier
        if [[ "$TIER1_ONLY" == "true" ]]; then
            local manifest="$img_dir/manifest.toml"
            if [[ -f "$manifest" ]] && ! grep -q 'tier.*critical' "$manifest" 2>/dev/null; then
                continue
            fi
        fi

        images+=("$name")
    done
    echo "${images[@]}"
}

# Main execution
main() {
    log_info "SBOM Enhancement from Source"
    log_info "Repository: $REPO_ROOT"
    log_info "Parallel: $PARALLEL"
    echo ""

    local images
    read -ra images <<< "$(get_images)"

    if [[ ${#images[@]} -eq 0 ]]; then
        log_warn "No images found to process"
        return 0
    fi

    log_info "Found ${#images[@]} images to process"
    echo ""

    local processed=0
    local enhanced=0
    local skipped=0
    local failed=0

    for img in "${images[@]}"; do
        processed=$((processed + 1))

        if [[ "$DRY_RUN" == "true" ]]; then
            log_info "[DRY-RUN] Processing $img ($processed/${#images[@]})"
        else
            log_info "Processing $img ($processed/${#images[@]})"
        fi

        if enhance_sbom "$img"; then
            enhanced=$((enhanced + 1))
        else
            skipped=$((skipped + 1))
        fi
    done

    echo ""
    log_info "Results:"
    log_info "  Processed: $processed"
    log_ok "  Enhanced: $enhanced"
    log_warn "  Skipped: $skipped"
    if [[ "$DRY_RUN" != "true" ]]; then
        log_info "  Output: $RESULTS_FILE"
    fi
}

main "$@"
