#!/usr/bin/env bash
# =============================================================================
# EVERGREEN IMAGE REGISTRY - DISCOVER SCRIPT
# =============================================================================
# Reads per-image manifest.toml files and the top-level manifest.toml to
# produce a JSON matrix suitable for GitHub Actions build jobs.
#
# Modes:
#   changed   - Images whose files changed in the last commit (default)
#   tier      - All images in a specific tier (critical|standard|community|experimental)
#   all       - All images, grouped by tier
#   images    - Specific comma-separated list of image names
#
# Usage:
#   ./scripts/discover-images.sh [mode] [filter]
#   ./scripts/discover-images.sh changed              # changed images only
#   ./scripts/discover-images.sh tier critical        # all critical images
#   ./scripts/discover-images.sh all                  # everything
#   ./scripts/discover-images.sh images nginx,redis   # specific images
#
# Output:
#   JSON matrix to stdout: {"include": [{"batch": 0, "images": "a,b,c", ...}]}
#   Image list to GITHUB_OUTPUT: images_json, tier_counts
# =============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGES_DIR="${REPO_ROOT}/images"
TOP_MANIFEST="${REPO_ROOT}/manifest.toml"
GITHUB_OUTPUT="${GITHUB_OUTPUT:-/dev/null}"

# ---------------------------------------------------------------------------
# Legacy tier mapping
# ---------------------------------------------------------------------------
resolve_tier() {
    local raw="$1"
    # Strip surrounding quotes if present
    raw="${raw#\"}"
    raw="${raw%\"}"
    case "$raw" in
        1) echo "critical" ;;
        2) echo "standard" ;;
        3) echo "community" ;;
        critical|standard|community|experimental) echo "$raw" ;;
        *) echo "standard" ;;  # default
    esac
}

# ---------------------------------------------------------------------------
# Read tier from a single image manifest
# ---------------------------------------------------------------------------
get_image_tier() {
    local manifest="$1"
    if [ -f "$manifest" ]; then
        local raw
        raw=$(grep '^tier = ' "$manifest" 2>/dev/null | head -1 | sed 's/^tier = //')
        if [ -n "$raw" ]; then
            resolve_tier "$raw"
            return
        fi
    fi
    echo "standard"  # default
}

# ---------------------------------------------------------------------------
# Read batch_size from top-level manifest
# ---------------------------------------------------------------------------
get_batch_size() {
    if [ -f "$TOP_MANIFEST" ]; then
        # Extract batch_size using grep (no TOML parser in CI)
        local val
        val=$(grep -oP 'batch_size\s*=\s*\K[0-9]+' "$TOP_MANIFEST" 2>/dev/null || echo "50")
        echo "${val:-50}"
    else
        echo "50"
    fi
}

# ---------------------------------------------------------------------------
# List all image directories that have a Dockerfile
# ---------------------------------------------------------------------------
list_all_images() {
    find "${IMAGES_DIR}" -maxdepth 2 -name Dockerfile \
        -not -path '*/__pycache__/*' \
        -not -path '*/tests/*' \
        -not -path '*/health-shim/*' \
        | sed "s|images/||" \
        | sed 's|/Dockerfile||' \
        | sort
}

# ---------------------------------------------------------------------------
# Get images changed in the last commit (or diff against base)
# ---------------------------------------------------------------------------
get_changed_images() {
    local base="${1:-HEAD~1}"
    local changed
    changed=$(git diff --name-only "${base}" HEAD -- "images/" 2>/dev/null \
        | grep "^images/" \
        | sed "s|images/||" \
        | sed 's|/.*||' \
        | sort -u)

    # Also check for changes to shared scripts, top-level manifest, or CI
    # If these changed, we should still only build affected images (not all)
    local shared_changed
    shared_changed=$(git diff --name-only "${base}" HEAD \
        -- scripts/ manifest.toml .github/workflows/build-on-push.yml \
        2>/dev/null || true)

    if [ -n "$changed" ]; then
        echo "$changed"
    elif [ -n "$shared_changed" ]; then
        # Shared infra changed but no specific images -- build critical tier
        list_all_images | while read -r img; do
            tier=$(get_image_tier "${IMAGES_DIR}/${img}/manifest.toml")
            if [ "$tier" = "critical" ]; then
                echo "$img"
            fi
        done
    fi
}

# ---------------------------------------------------------------------------
# Filter images by tier
# ---------------------------------------------------------------------------
get_tier_images() {
    local target_tier="$1"
    list_all_images | while read -r img; do
        tier=$(get_image_tier "${IMAGES_DIR}/${img}/manifest.toml")
        if [ "$tier" = "$target_tier" ]; then
            echo "$img"
        fi
    done
}

# ---------------------------------------------------------------------------
# Get specific images by name
# ---------------------------------------------------------------------------
get_specific_images() {
    local IFS=','
    read -ra NAMES <<< "$1"
    for name in "${NAMES[@]}"; do
        name=$(echo "$name" | xargs)  # trim whitespace
        if [ -f "${IMAGES_DIR}/${name}/Dockerfile" ]; then
            echo "$name"
        else
            echo "::warning::Image '${name}' not found, skipping" >&2
        fi
    done | sort -u
}

# ---------------------------------------------------------------------------
# Create batched JSON matrix from image list
# ---------------------------------------------------------------------------
create_matrix() {
    local batch_size="$1"
    shift
    local images=("$@")

    if [ ${#images[@]} -eq 0 ]; then
        echo '{"include":[]}'
        return
    fi

    python3 - <<PYEOF
import json, os, sys

batch_size = ${batch_size}
images = $(printf '%s\n' "${images[@]}" | python3 -c "import json,sys; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))")

if not images:
    print(json.dumps({"include": []}))
    sys.exit(0)

batches = []
for i in range(0, len(images), batch_size):
    chunk = images[i:i + batch_size]
    batches.append({
        "batch": i // batch_size,
        "images": ",".join(chunk),
        "count": len(chunk),
    })

print(json.dumps({"include": batches}))
PYEOF
}

# ---------------------------------------------------------------------------
# Count images per tier (for reporting)
# ---------------------------------------------------------------------------
count_tiers() {
    list_all_images | while read -r img; do
        tier=$(get_image_tier "${IMAGES_DIR}/${img}/manifest.toml")
        echo "$tier"
    done | sort | uniq -c
}

# =============================================================================
# MAIN
# =============================================================================
MODE="${1:-changed}"
FILTER="${2:-}"

BATCH_SIZE=$(get_batch_size)

case "$MODE" in
    changed)
        IMAGES=$(get_changed_images "HEAD~1")
        ;;
    tier)
        if [ -z "$FILTER" ]; then
            echo "ERROR: tier mode requires a tier name (critical|standard|community|experimental)" >&2
            exit 1
        fi
        IMAGES=$(get_tier_images "$FILTER")
        ;;
    all)
        IMAGES=$(list_all_images)
        ;;
    images)
        if [ -z "$FILTER" ]; then
            echo "ERROR: images mode requires comma-separated image names" >&2
            exit 1
        fi
        IMAGES=$(get_specific_images "$FILTER")
        ;;
    *)
        echo "ERROR: unknown mode '${MODE}'. Use: changed|tier|all|images" >&2
        exit 1
        ;;
esac

# Convert to array
mapfile -t IMAGE_ARRAY <<< "$IMAGES"
# Remove empty entries
IMAGE_ARRAY=("${IMAGE_ARRAY[@]##*( )}")
IMAGE_ARRAY=("${IMAGE_ARRAY[@]%%*( )}")

TOTAL=${#IMAGE_ARRAY[@]}

if [ "$TOTAL" -eq 0 ]; then
    echo "::notice::No images to build in mode=${MODE} filter=${FILTER}"
    MATRIX='{"include":[]}'
else
    MATRIX=$(create_matrix "$BATCH_SIZE" "${IMAGE_ARRAY[@]}")
fi

# Output matrix to stdout (captured by CI)
echo "$MATRIX"

# Write to GITHUB_OUTPUT for downstream steps
if [ "$GITHUB_OUTPUT" != "/dev/null" ]; then
    {
        echo "matrix=${MATRIX}"
        echo "total=${TOTAL}"
        echo "mode=${MODE}"
        echo "filter=${FILTER}"
    } >> "$GITHUB_OUTPUT"

    # Tier counts
    {
        echo "tier_counts<<TIEREOF"
        count_tiers
        echo "TIEREOF"
    } >> "$GITHUB_OUTPUT"
fi

echo "::notice::Mode=${MODE}, Filter=${FILTER:-none}, Total=${TOTAL}, BatchSize=${BATCH_SIZE}" >&2
