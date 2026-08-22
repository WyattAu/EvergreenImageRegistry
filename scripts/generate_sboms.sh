#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry - SBOM Generator
# =============================================================================
# Generates SPDX 2.3 SBOMs for all images using Syft.
# Tries GHCR pull first, falls back to local build.
#
# Usage:
#   bash scripts/generate_sboms.sh [--force] [--image <name>] [--batch <n>]
#
# Options:
#   --force     Regenerate even if SBOM exists
#   --image     Generate SBOM for specific image only
#   --batch     Process in batches of N (default: all)
# =============================================================================

set -euo pipefail

SYFT="/usr/local/bin/syft"

# Install syft if not available
if ! command -v "$SYFT" &>/dev/null; then
    echo "Installing Syft..."
    curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
    SYFT="/usr/local/bin/syft"
fi
FORCE=false
IMAGE_FILTER=""
BATCH_SIZE=0
GENERATED=0
SKIPPED=0
FAILED=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --force) FORCE=true; shift ;;
        --image) IMAGE_FILTER="$2"; shift 2 ;;
        --batch) BATCH_SIZE="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

echo "=========================================="
echo "Evergreen SBOM Generator"
echo "=========================================="
echo "Syft version: $($SYFT version 2>/dev/null | head -1)"
echo "Force: $FORCE"
echo ""

# Find target images
find images -maxdepth 1 -type d \
    ! -name images \
    ! -name '_wip' \
    ! -name '_archive' \
    ! -name 'tests' \
    | sed 's|images/||' | sort > /tmp/all-images.txt

if [ -n "$IMAGE_FILTER" ]; then
    grep "^${IMAGE_FILTER}$" /tmp/all-images.txt > /tmp/target-images.txt || {
        echo "Image not found: $IMAGE_FILTER"
        exit 1
    }
else
    cp /tmp/all-images.txt /tmp/target-images.txt
fi

# Filter out images with existing SBOMs (unless --force)
if [ "$FORCE" != "true" ]; then
    while IFS= read -r img; do
        if [ -f "images/${img}/sbom.spdx.json" ]; then
            SKIPPED=$((SKIPPED + 1))
            continue
        fi
        echo "$img"
    done < /tmp/target-images.txt > /tmp/pending-images.txt
else
    cp /tmp/target-images.txt /tmp/pending-images.txt
fi

TOTAL=$(wc -l < /tmp/pending-images.txt)
echo "Target images: $(wc -l < /tmp/target-images.txt)"
echo "Pending SBOMs: $TOTAL"
echo ""

if [ "$TOTAL" -eq 0 ]; then
    echo "No images need SBOM generation."
    exit 0
fi

# Process images
COUNT=0
while IFS= read -r img; do
    [ -z "$img" ] && continue
    COUNT=$((COUNT + 1))

    # Apply batch limit
    if [ "$BATCH_SIZE" -gt 0 ] && [ "$COUNT" -gt "$BATCH_SIZE" ]; then
        echo ""
        echo "Batch limit reached ($BATCH_SIZE images)"
        break
    fi

    echo -n "[${COUNT}/${TOTAL}] ${img}: "

    # Skip if no Dockerfile
    if [ ! -f "images/${img}/Dockerfile" ]; then
        echo "SKIP (no Dockerfile)"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    # Try to pull from GHCR
    REF="ghcr.io/wyattau/evergreenimageregistry/${img}:latest"
    if docker pull "$REF" > /dev/null 2>&1; then
        if $SYFT "$REF" -o spdx-json="images/${img}/sbom.spdx.json" > /dev/null 2>&1; then
            echo "OK (from GHCR)"
            GENERATED=$((GENERATED + 1))
        else
            echo "FAIL (Syft error)"
            FAILED=$((FAILED + 1))
        fi
    else
        # Build locally
        echo -n "building... "
        if docker build -t "sbom-temp:${img}" "images/${img}" > /dev/null 2>&1; then
            if $SYFT "sbom-temp:${img}" -o spdx-json="images/${img}/sbom.spdx.json" > /dev/null 2>&1; then
                echo "OK (local build)"
                GENERATED=$((GENERATED + 1))
            else
                echo "FAIL (Syft error)"
                FAILED=$((FAILED + 1))
            fi
            docker rmi "sbom-temp:${img}" > /dev/null 2>&1 || true
        else
            echo "FAIL (build error)"
            FAILED=$((FAILED + 1))
        fi
    fi
done < /tmp/pending-images.txt

echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="
echo "Generated: $GENERATED"
echo "Skipped:   $SKIPPED"
echo "Failed:    $FAILED"
echo "Total SBOMs: $(find images -maxdepth 2 -name 'sbom.spdx.json' ! -path '*_wip*' ! -path '*_archive*' | wc -l)"
echo "=========================================="
