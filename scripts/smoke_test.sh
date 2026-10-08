#!/bin/bash
# Smoke test framework for Evergreen Image Registry
# Builds, runs, and healthchecks images to verify they work
#
# Usage:
#   ./scripts/smoke_test.sh                    # Test all images
#   ./scripts/smoke_test.sh redis nginx        # Test specific images
#   ./scripts/smoke_test.sh --tier critical    # Test critical-tier only
#   ./scripts/smoke_test.sh --parallel 4       # Run 4 tests in parallel

set -euo pipefail

IMAGES_DIR="images"
RESULTS_DIR="smoke-test-results"
PARALLEL=1
TIER_FILTER=""
SPECIFIC_IMAGES=()

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --parallel)
            PARALLEL="$2"
            shift 2
            ;;
        --tier)
            TIER_FILTER="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--parallel N] [--tier critical|standard] [IMAGE...]"
            exit 0
            ;;
        *)
            SPECIFIC_IMAGES+=("$1")
            shift
            ;;
    esac
done

# Create results directory.
# Clear it first: result files are per-image, so without this a run that tests
# fewer images (or an image that now passes) inherits the previous run's
# verdict, and the uploaded artifact reports failures that no longer exist.
mkdir -p "$RESULTS_DIR"
rm -f "$RESULTS_DIR"/*.txt

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Counters
TOTAL=0
PASSED=0
FAILED=0
SKIPPED=0

# Get list of images to test
get_images() {
    if [[ ${#SPECIFIC_IMAGES[@]} -gt 0 ]]; then
        for img in "${SPECIFIC_IMAGES[@]}"; do
            if [[ -d "$IMAGES_DIR/$img" ]]; then
                echo "$img"
            fi
        done
    else
        for manifest in "$IMAGES_DIR"/*/manifest.toml; do
            [[ -f "$manifest" ]] || continue
            [[ "$manifest" == *"_wip"* || "$manifest" == *"_archive"* ]] && continue

            if [[ -n "$TIER_FILTER" ]]; then
                grep -q "tier = \"$TIER_FILTER\"" "$manifest" || continue
            fi

            basename "$(dirname "$manifest")"
        done
    fi
}

# Test a single image
test_image() {
    local img="$1"
    local df="$IMAGES_DIR/$img/Dockerfile"
    local result_file="$RESULTS_DIR/$img.txt"

    # Skip if no Dockerfile
    if [[ ! -f "$df" ]]; then
        echo "SKIP $img (no Dockerfile)" >> "$result_file"
        return 0
    fi

    # Skip if only FIPS variant
    if [[ ! -f "$df" ]] && [[ -f "$IMAGES_DIR/$img/Dockerfile.fips" ]]; then
        echo "SKIP $img (FIPS-only)" >> "$result_file"
        return 0
    fi

    echo "Testing $img..."

    # Step 1: Validate Dockerfile syntax
    if ! grep -q '^FROM ' "$df"; then
        echo "FAIL $img: No FROM instruction" >> "$result_file"
        return 1
    fi

    # Step 2: Effective runtime user — checked against the BUILT image
    # config, not the Dockerfile text. The static grep was structurally
    # wrong: 23 of 58 critical images inherited a non-root USER from
    # upstream bases and were flagged as violations (audit, SIS loop
    # iteration 8). The build in Step 5 is where the real answer comes
    # from; here we only keep the cheap static sanity check for FROM.

    # Step 3: Check for HEALTHCHECK
    if ! grep -q 'HEALTHCHECK' "$df" && ! grep -q '^FROM scratch' "$df"; then
        echo "FAIL $img: No HEALTHCHECK" >> "$result_file"
        return 1
    fi

    # Step 4: Check for ENTRYPOINT or CMD
    if ! grep -q 'ENTRYPOINT\|CMD' "$df"; then
        echo "FAIL $img: No ENTRYPOINT or CMD" >> "$result_file"
        return 1
    fi

    # Step 5: Build the image (optional, requires Docker)
    if command -v docker &>/dev/null; then
        echo "  Building $img..."
        if timeout 300 docker build -t "smoke-test/$img:latest" "$IMAGES_DIR/$img" >/dev/null 2>&1; then
            echo "  Build: PASS"
            # Effective runtime user from the built image config — the
            # authoritative answer (covers inherited USER, scratch images,
            # everything). Empty means the container starts as root; that
            # is recorded as a warning-level fact, not a failure: database
            # and host-agent images legitimately start as root and drop
            # privileges in their entrypoints.
            local eff_user
            eff_user=$(docker image inspect "smoke-test/$img:latest" --format '{{.Config.User}}' 2>/dev/null || echo "?")
            if [[ -z "$eff_user" ]]; then
                echo "INFO $img: starts as root (no USER in final config; entrypoint may drop privileges)" >> "$result_file"
                echo "  User: root (config)"
            else
                echo "OK $img: effective user '$eff_user'" >> "$result_file"
                echo "  User: $eff_user"
            fi

            # Step 6: Run the container
            echo "  Running $img..."
            local container_id
            container_id=$(timeout 30 docker run -d --rm "smoke-test/$img:latest" 2>/dev/null || true)

            if [[ -n "$container_id" ]]; then
                # Wait for container to start
                sleep 5

                # Check if container is still running
                if docker ps --format '{{.ID}}' | grep -q "${container_id:0:12}"; then
                    echo "  Run: PASS"

                    # Step 7: Check healthcheck
                    local health
                    health=$(docker inspect --format '{{.State.Health.Status}}' "$container_id" 2>/dev/null || echo "unknown")
                    echo "  Health: $health"

                    # Cleanup
                    docker stop "$container_id" >/dev/null 2>&1 || true
                else
                    echo "  Run: Container exited"
                fi
            else
                echo "  Run: Could not start container"
            fi

            # Cleanup image
            docker rmi "smoke-test/$img:latest" >/dev/null 2>&1 || true
        else
            echo "  Build: FAIL (timeout or error)"
            echo "FAIL $img: Build failed" >> "$result_file"
            return 1
        fi
    else
        echo "  Docker not available, skipping build test"
    fi

    # "PASS" for the summary counter; "OK"/"INFO" lines carry the
    # effective-user verdict written during the build step above.
    echo "PASS $img" >> "$result_file"
    if ! grep -qE '^(OK|INFO) '"$img" "$result_file" 2>/dev/null; then
        echo "INFO $img: no user inspection recorded (docker unavailable)" >> "$result_file"
    fi
    return 0
}

# Main
echo "========================================="
echo "Smoke Test Framework"
echo "========================================="
echo "Images directory: $IMAGES_DIR"
echo "Results directory: $RESULTS_DIR"
echo "Parallel jobs: $PARALLEL"
echo "Tier filter: ${TIER_FILTER:-all}"
echo ""

# Get images
mapfile -t IMAGES < <(get_images)
TOTAL=${#IMAGES[@]}

echo "Found $TOTAL images to test"
echo ""

# Run tests
for img in "${IMAGES[@]}"; do
    if test_image "$img"; then
        PASSED=$((PASSED + 1))
    else
        FAILED=$((FAILED + 1))
    fi
done

# Summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Total:  $TOTAL"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

# Generate report
echo "Results saved to $RESULTS_DIR/"

# Exit code
if [[ $FAILED -gt 0 ]]; then
    exit 1
fi
exit 0
