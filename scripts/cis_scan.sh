#!/bin/bash
# CIS Docker Benchmark Scanner for EIR Images
# Based on CIS Docker Benchmark v1.6.0

set -euo pipefail

REGISTRY="ghcr.io/wyattau/evergreenimageregistry"
RESULTS_DIR="compliance/cis/results"
mkdir -p "$RESULTS_DIR"

scan_image() {
    local img="$1"
    local ref="${REGISTRY}/${img}:latest"
    local result_file="${RESULTS_DIR}/${img}.json"
    local pass=0
    local fail=0
    local warn=0
    
    # Check if image exists
    if ! docker manifest inspect "$ref" >/dev/null 2>&1; then
        return
    fi
    
    # CIS 4.1: Create a non-root user for the container
    local user
    user=$(docker inspect --format '{{.Config.User}}' "$ref" 2>/dev/null || echo "")
    if [[ -n "$user" ]] && [[ "$user" != "root" ]] && [[ "$user" != "0" ]]; then
        pass=$((pass+1))
        user_check="PASS"
    else
        fail=$((fail+1))
        user_check="FAIL"
    fi
    
    # CIS 4.6: Add HEALTHCHECK instruction to the container image
    local healthcheck
    healthcheck=$(docker inspect --format '{{.Config.Healthcheck.Test}}' "$ref" 2>/dev/null || echo "none")
    if [[ "$healthcheck" != "none" ]] && [[ "$healthcheck" != "[]" ]]; then
        pass=$((pass+1))
        hc_check="PASS"
    else
        warn=$((warn+1))
        hc_check="WARN"
    fi
    
    # CIS 4.7: Do not update packages in the container image (check for apt-get upgrade)
    # This is a build-time check, skip at runtime
    
    # CIS 4.8: Confirm packages are removed after use
    # This is a build-time check, skip at runtime
    
    # Check for setuid/setgid files
    local suid_count
    suid_count=$(docker run --rm --entrypoint "" "$ref" sh -c "find / -perm -4000 -type f 2>/dev/null | wc -l" 2>/dev/null || echo "unknown")
    if [[ "$suid_count" == "0" ]]; then
        pass=$((pass+1))
        suid_check="PASS"
    elif [[ "$suid_count" == "unknown" ]]; then
        warn=$((warn+1))
        suid_check="WARN"
    else
        fail=$((fail+1))
        suid_check="FAIL ($suid_count suid files)"
    fi
    
    # Check for shell access
    local has_shell
    has_shell=$(docker run --rm --entrypoint "" "$ref" sh -c "echo SHELL_EXISTS" 2>/dev/null || echo "NO_SHELL")
    if [[ "$has_shell" == "NO_SHELL" ]]; then
        pass=$((pass+1))
        shell_check="PASS (no shell)"
    else
        warn=$((warn+1))
        shell_check="WARN (shell present)"
    fi
    
    cat > "$result_file" << EOF
{
  "image": "$img",
  "scanned_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "checks": {
    "non_root_user": "$user_check",
    "healthcheck": "$hc_check",
    "no_suid_files": "$suid_check",
    "no_shell": "$shell_check"
  },
  "summary": {
    "pass": $pass,
    "fail": $fail,
    "warn": $warn
  }
}
EOF
    echo "$img: $pass pass, $fail fail, $warn warn"
}

echo "=== CIS Docker Benchmark Scan ==="
for img in redis nginx traefik prometheus alertmanager grafana oauth2-proxy keycloak postgresql-16 mariadb nats node-exporter blackbox-exporter; do
    scan_image "$img" || true
done

# Summary
echo ""
echo "=== Summary ==="
total_pass=$(grep -oh '"pass": [0-9]*' ${RESULTS_DIR}/*.json 2>/dev/null | awk -F': ' '{s+=$2} END {print s+0}')
total_fail=$(grep -oh '"fail": [0-9]*' ${RESULTS_DIR}/*.json 2>/dev/null | awk -F': ' '{s+=$2} END {print s+0}')
total_warn=$(grep -oh '"warn": [0-9]*' ${RESULTS_DIR}/*.json 2>/dev/null | awk -F': ' '{s+=$2} END {print s+0}')
echo "Total: $total_pass pass, $total_fail fail, $total_fail warn"
