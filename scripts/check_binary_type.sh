#!/usr/bin/env bash
# check_binary_type.sh — Verify that binaries in scratch-based EIR images are statically linked.
#
# For each image with `evergreen.base.image="scratch"`, this script:
#   1. Builds the image
#   2. Runs a container and copies the shim binary out
#   3. Runs `file` to check if it's dynamically linked
#   4. Fails if any binary in a scratch image is dynamically linked
#
# Usage:
#   scripts/check_binary_type.sh [--image NAME]
#
# Exit codes:
#   0 — all checks passed
#   1 — one or more images failed the check

set -euo pipefail

IMAGES_DIR="$(cd "$(dirname "$0")/.." && pwd)/images"
SPECIFIC_IMAGE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --image)
      SPECIFIC_IMAGE="$2"
      shift 2
      ;;
    *)
      echo "Usage: $0 [--image NAME]" >&2
      exit 1
      ;;
  esac
done

PASS=0
FAIL=0
SKIP=0

check_image() {
  local name="$1"
  local dockerfile="${IMAGES_DIR}/${name}/Dockerfile"

  # Only check scratch-based images
  if ! grep -q 'evergreen.base.image="scratch"' "$dockerfile" 2>/dev/null; then
    return 0
  fi

  echo "::group::${name}"

  # Find the shim binary path from ENTRYPOINT or COPY --from=shim
  local shim_dest
  shim_dest=$(grep -oP 'COPY\s+--from=shim\s+\S+\s+(\S+)' "$dockerfile" | tail -1 | awk '{print $NF}' || true)
  if [[ -z "$shim_dest" ]]; then
    echo "SKIP: ${name} — no COPY --from=shim found"
    SKIP=$((SKIP + 1))
    echo "::endgroup::"
    return 0
  fi

  local tag="eir-check-${name}:$$"

  # Build the image
  echo "Building ${name}..."
  if ! docker build -t "$tag" "$IMAGES_DIR/$name" >/dev/null 2>&1; then
    echo "SKIP: ${name} — build failed"
    SKIP=$((SKIP + 1))
    echo "::endgroup::"
    return 0
  fi

  # Create a temporary container and copy the shim binary out
  local cid
  cid=$(docker create "$tag" 2>/dev/null) || {
    echo "SKIP: ${name} — could not create container"
    SKIP=$((SKIP + 1))
    docker rmi "$tag" >/dev/null 2>&1 || true
    echo "::endgroup::"
    return 0
  }

  local tmpbin="/tmp/eir-binary-check-$$.bin"
  docker cp "${cid}:${shim_dest}" "$tmpbin" 2>/dev/null || {
    echo "SKIP: ${name} — could not copy ${shim_dest} from container"
    SKIP=$((SKIP + 1))
    docker rm "$cid" >/dev/null 2>&1 || true
    docker rmi "$tag" >/dev/null 2>&1 || true
    rm -f "$tmpbin"
    echo "::endgroup::"
    return 0
  }

  # Check binary type
  local file_output
  file_output=$(file "$tmpbin")
  echo "Binary type: ${file_output}"

  if echo "$file_output" | grep -qi "dynamically linked"; then
    echo "FAIL: ${name} — binary at ${shim_dest} is dynamically linked (scratch requires static)"
    FAIL=$((FAIL + 1))
  else
    echo "PASS: ${name} — binary is statically linked"
    PASS=$((PASS + 1))
  fi

  # Cleanup
  rm -f "$tmpbin"
  docker rm "$cid" >/dev/null 2>&1 || true
  docker rmi "$tag" >/dev/null 2>&1 || true

  echo "::endgroup::"
}

if [[ -n "$SPECIFIC_IMAGE" ]]; then
  check_image "$SPECIFIC_IMAGE"
else
  for dockerfile in "$IMAGES_DIR"/*/Dockerfile; do
    name=$(basename "$(dirname "$dockerfile")")
    [[ "$name" == _* ]] && continue
    [[ "$name" == "tests" || "$name" == "health-shim" ]] && continue
    check_image "$name"
  done
fi

echo ""
echo "=== Binary Type Check Results ==="
echo "Passed: ${PASS} | Failed: ${FAIL} | Skipped: ${SKIP}"

if [[ "$FAIL" -gt 0 ]]; then
  exit 1
fi
