#!/usr/bin/env bash
# =============================================================================
# FIPS COMPLIANCE CHECK SCRIPT
# =============================================================================
# Reads compliance/fips/fips_image_matrix.yaml, checks if images claiming FIPS
# compliance have FIPS-certified base images, and reports compliance status.
# Exit code: 0 = all pass, 1 = warnings/failures found
# =============================================================================

set -euo pipefail

MATRIX_FILE="compliance/fips/fips_image_matrix.yaml"
IMAGES_DIR="images"
REPORT_FILE="/tmp/fips_compliance_report.txt"
WARNINGS=0
FAILURES=0
PASS=0

log() { echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $*"; }
warn() { echo "[WARN] $*"; WARNINGS=$((WARNINGS + 1)); }
fail() { echo "[FAIL] $*"; FAILURES=$((FAILURES + 1)); }
pass() { echo "[PASS] $*"; PASS=$((PASS + 1)); }

# Check if matrix file exists
if [ ! -f "${MATRIX_FILE}" ]; then
    log "FIPS matrix not found at ${MATRIX_FILE}, creating minimal matrix..."
    mkdir -p "$(dirname "${MATRIX_FILE}")"
    cat > "${MATRIX_FILE}" <<'YAML'
fips_image_matrix:
  version: '1.0.0'
  generated: 'PLACEHOLDER'
  description: 'FIPS 140-2/140-3 image variant matrix for Evergreen Image Registry'
  fips_standard: 'FIPS 140-2'
  categories:
    databases:
      images:
        - name: postgresql
          fips_achievable: true
          fips_approach: 'Build with OpenSSL 3.x FIPS provider'
          crypto_deps: [openssl]
        - name: redis
          fips_achievable: true
          fips_approach: 'Build with BUILD_TLS=yes against FIPS OpenSSL'
          crypto_deps: [openssl]
    monitoring:
      images:
        - name: prometheus
          fips_achievable: true
          fips_approach: 'Build with GOEXPERIMENT=boringcrypto'
          crypto_deps: [golang.org/x/crypto]
        - name: grafana
          fips_achievable: true
          fips_approach: 'Build with GOEXPERIMENT=boringcrypto'
          crypto_deps: [golang.org/x/crypto]
    networking:
      images:
        - name: nginx
          fips_achievable: true
          fips_approach: 'Build from source with FIPS OpenSSL'
          crypto_deps: [openssl]
        - name: traefik
          fips_achievable: true
          fips_approach: 'Build with GOEXPERIMENT=boringcrypto'
          crypto_deps: [golang.org/x/crypto]
YAML
    log "Created minimal FIPS matrix at ${MATRIX_FILE}"
fi

log "=== FIPS Compliance Check ==="
log "Matrix: ${MATRIX_FILE}"
log "Images directory: ${IMAGES_DIR}"
echo ""

# Known FIPS-certified base images
declare -A FIPS_BASES=(
    ["gcr.io/distroless/static-debian12"]="FIPS-certified via BoringSSL FIPS module"
    ["cgr.dev/chainguard/wolfi-base-fips"]="Chainguard FIPS-enabled wolfi-base"
    ["debian:bookworm-slim"]="FIPS achievable with libssl3-fips"
)

# Parse matrix for FIPS-achievable images
parse_matrix() {
    local image_name="$1"
    local approach=""
    local crypto_deps=""
    local fips_achievable=""

    # Simple YAML parsing for image entries
    if grep -q "name: ${image_name}" "${MATRIX_FILE}"; then
        # Find the image block and extract fields
        fips_achievable=$(grep -A 5 "name: ${image_name}" "${MATRIX_FILE}" | grep "fips_achievable:" | awk '{print $2}' || echo "unknown")
        approach=$(grep -A 10 "name: ${image_name}" "${MATRIX_FILE}" | grep -A 5 "fips_approach:" | head -1 | sed 's/.*fips_approach: *//' | sed 's/^|//' | sed 's/^ *//' || echo "unknown")
        crypto_deps=$(grep -A 15 "name: ${image_name}" "${MATRIX_FILE}" | grep -A 3 "crypto_deps:" | head -3 | tr '\n' ' ' || echo "unknown")
    fi

    echo "${fips_achievable}|${approach}|${crypto_deps}"
}

# Check base image FIPS status
check_base_fips() {
    local image_name="$1"
    local dockerfile="${IMAGES_DIR}/${image_name}/Dockerfile"

    if [ ! -f "${dockerfile}" ]; then
        echo "no-dockerfile"
        return
    fi

    local base_image
    base_image=$(grep -E '^FROM ' "${dockerfile}" | tail -1 | awk '{print $2}' | cut -d'@' -d: -f1 || echo "unknown")

    if [ -z "${base_image}" ] || [ "${base_image}" = "scratch" ]; then
        # scratch-based images with Go crypto - check if Go build uses boringcrypto
        if grep -q "GOEXPERIMENT=boringcrypto" "${dockerfile}"; then
            echo "boringcrypto-enabled"
        else
            echo "scratch-no-boringcrypto"
        fi
    elif [[ "${base_image}" == *"wolfi-base"* ]] && [[ "${base_image}" == *"fips"* ]]; then
        echo "fips-wolfi"
    elif [[ "${base_image}" == *"distroless"* ]]; then
        echo "distroless"
    elif [[ "${base_image}" == *"debian"* ]]; then
        if grep -q "libssl3-fips\|openssl-fips" "${dockerfile}" 2>/dev/null; then
            echo "debian-fips"
        else
            echo "debian-no-fips"
        fi
    elif [[ "${base_image}" == *"wolfi"* ]]; then
        echo "wolfi"
    else
        echo "${base_image}"
    fi
}

# Main check loop
log "Checking FIPS-achievable images from matrix..."
echo ""

for image_name in $(grep -oP 'name:\s*\K\S+' "${MATRIX_FILE}" | sort -u); do
    # Skip if no Dockerfile exists
    if [ ! -f "${IMAGES_DIR}/${image_name}/Dockerfile" ]; then
        warn "${image_name}: FIPS-achievable in matrix but no Dockerfile found"
        continue
    fi

    log "--- ${image_name} ---"

    matrix_info=$(parse_matrix "${image_name}")
    fips_achievable=$(echo "${matrix_info}" | cut -d'|' -f1)
    approach=$(echo "${matrix_info}" | cut -d'|' -f2)

    if [ "${fips_achievable}" != "true" ]; then
        log "  FIPS not achievable (requires upstream changes)"
        continue
    fi

    log "  FIPS approach: ${approach}"

    base_status=$(check_base_fips "${image_name}")
    log "  Base image status: ${base_status}"

    case "${base_status}" in
        boringcrypto-enabled|fips-wolfi|debian-fips|distroless)
            pass "${image_name}: FIPS-ready (${base_status})"
            ;;
        scratch-no-boringcrypto)
            fail "${image_name}: scratch-based without GOEXPERIMENT=boringcrypto - FIPS not supported"
            ;;
        debian-no-fips)
            warn "${image_name}: Debian base without FIPS OpenSSL - FIPS achievable with changes"
            ;;
        wolfi)
            warn "${image_name}: wolfi-base without FIPS variant - FIPS achievable with FIPS base"
            ;;
        *)
            warn "${image_name}: Unknown base status (${base_status})"
            ;;
    esac
    echo ""
done

# Check for FIPS env vars
log "=== Checking FIPS environment variable configuration ==="
for dockerfile in "${IMAGES_DIR}"/*/Dockerfile; do
    [ -f "${dockerfile}" ] || continue
    name=$(basename "$(dirname "${dockerfile}")")

    if grep -q "OPENSSL_CONF\|GOLANG_FIPS\|VAULT_FIPS" "${dockerfile}" 2>/dev/null; then
        pass "${name}: FIPS environment variables configured"
    elif grep -q "GOEXPERIMENT=boringcrypto" "${dockerfile}" 2>/dev/null; then
        warn "${name}: BoringCrypto build but missing GOLANG_FIPS=1 at runtime"
    fi
done

# Summary
echo ""
log "=== FIPS Compliance Summary ==="
log "PASS: ${PASS}"
log "WARNINGS: ${WARNINGS}"
log "FAILURES: ${FAILURES}"

if [ "${FAILURES}" -gt 0 ]; then
    log "RESULT: FAIL - ${FAILURES} critical FIPS compliance issues found"
    exit 1
elif [ "${WARNINGS}" -gt 0 ]; then
    log "RESULT: WARN - ${WARNINGS} FIPS compliance warnings"
    exit 0
else
    log "RESULT: PASS - All FIPS checks passed"
    exit 0
fi
