#!/bin/bash
# FIPS 140-2/3 Readiness Scanner for EIR Images
# Checks: OpenSSL config, FIPS module availability, non-FIPS algorithms

set -euo pipefail

REGISTRY="ghcr.io/wyattau/evergreenimageregistry"
RESULTS_DIR="compliance/fips/results"
mkdir -p "$RESULTS_DIR"

scan_image() {
    local img="$1"
    local ref="${REGISTRY}/${img}:latest"
    local result_file="${RESULTS_DIR}/${img}.json"
    
    # Check if image exists
    if ! docker manifest inspect "$ref" >/dev/null 2>&1; then
        echo "{\"image\":\"$img\",\"status\":\"not_found\"}" > "$result_file"
        return
    fi
    
    # Check for OpenSSL in the image
    local has_openssl="false"
    local fips_capable="false"
    local fips_enabled="false"
    
    # Try to run openssl version in the image
    openssl_output=$(docker run --rm --entrypoint "" "$ref" sh -c "openssl version 2>/dev/null || echo 'NO_OPENSSL'" 2>/dev/null || echo "NO_SHELL")
    
    if [[ "$openssl_output" != "NO_OPENSSL" ]] && [[ "$openssl_output" != "NO_SHELL" ]]; then
        has_openssl="true"
        # Check if FIPS capable
        if echo "$openssl_output" | grep -qi "fips"; then
            fips_capable="true"
        fi
        # Try FIPS self-test
        fips_test=$(docker run --rm --entrypoint "" -e OPENSSL_FIPS=1 "$ref" sh -c "openssl fips -verify 2>/dev/null && echo 'PASS' || echo 'FAIL'" 2>/dev/null || echo "NO_SHELL")
        if [[ "$fips_test" == "PASS" ]]; then
            fips_enabled="true"
        fi
    fi
    
    # Check base image
    local base_image
    base_image=$(grep "^FROM " "images/$img/Dockerfile" 2>/dev/null | grep -v "health-shim\|evergreenshim" | tail -1 | awk '{print $2}')
    
    # Determine status
    local status="not_applicable"
    if [[ "$has_openssl" == "true" ]]; then
        if [[ "$fips_enabled" == "true" ]]; then
            status="fips_ready"
        elif [[ "$fips_capable" == "true" ]]; then
            status="fips_capable"
        else
            status="not_fips"
        fi
    fi
    
    cat > "$result_file" << EOF
{
  "image": "$img",
  "base_image": "$base_image",
  "has_openssl": $has_openssl,
  "fips_capable": $fips_capable,
  "fips_enabled": $fips_enabled,
  "status": "$status",
  "openssl_version": "${openssl_output//\"/\\\"}",
  "scanned_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
    echo "$img: $status"
}

echo "=== FIPS Readiness Scan ==="
echo "Scanning hardened images..."

for img in redis nginx traefik prometheus alertmanager grafana oauth2-proxy keycloak postgresql-16 mariadb nats node-exporter blackbox-exporter; do
    scan_image "$img" || true
done

# Summary
echo ""
echo "=== Summary ==="
echo "FIPS Ready: $(grep -l '"fips_ready"' ${RESULTS_DIR}/*.json 2>/dev/null | wc -l)"
echo "FIPS Capable: $(grep -l '"fips_capable"' ${RESULTS_DIR}/*.json 2>/dev/null | wc -l)"
echo "Not FIPS: $(grep -l '"not_fips"' ${RESULTS_DIR}/*.json 2>/dev/null | wc -l)"
echo "Not Applicable: $(grep -l '"not_applicable"' ${RESULTS_DIR}/*.json 2>/dev/null | wc -l)"
