#!/usr/bin/env bash
# =============================================================================
# RUNTIME VERIFICATION TEST PLAN - CRITICAL EIR IMAGES ON TRUENAS
# =============================================================================
# SSHs into TrueNAS, verifies critical EIR containers are healthy, responsive,
# stable, and shut down gracefully. Outputs a structured report.
#
# Usage:
#   ./scripts/runtime-verify.sh [--host HOST] [--user USER] [--report PATH]
#
# Requirements:
#   - SSH access to TrueNAS (key-based auth)
#   - Docker 29.x on TrueNAS
#   - Containers already deployed via SIS stacks
# =============================================================================
set -euo pipefail

# --- Configuration ---
TRUENAS_HOST="${TRUENAS_HOST:-192.168.1.3}"
TRUENAS_USER="${TRUENAS_USER:-wyatt}"
SHIM_PORT=9101
REPORT_DIR="${REPORT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/.reports}"
TIMESTAMP=$(date -u '+%Y%m%dT%H%M%SZ')
REPORT_FILE="${REPORT_DIR}/runtime-verify-${TIMESTAMP}.md"
SSH_TIMEOUT=10

# Ordered list for deterministic output
CRITICAL_ORDER=(traefik postgres redis grafana keycloak forgejo cloudflared)

# --- State ---
PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0
RESULTS=()

# --- Helpers ---
log()  { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*" >&2; }
pass() { ((PASS_COUNT++)); RESULTS+=("PASS|$1|$2"); log "PASS  $1: $2"; }
fail() { ((FAIL_COUNT++)); RESULTS+=("FAIL|$1|$2"); log "FAIL  $1: $2"; }
warn() { ((WARN_COUNT++)); RESULTS+=("WARN|$1|$2"); log "WARN  $1: $2"; }

ssh_cmd() {
    ssh -o ConnectTimeout="${SSH_TIMEOUT}" \
        -o StrictHostKeyChecking=accept-new \
        "${TRUENAS_USER}@${TRUENAS_HOST}" \
        "$@"
}

# Find the running container for a given service
find_container() {
    local service="$1"
    local patterns=("${service}" "${service}-1" "${service}-server" "${service}_1")
    for pat in "${patterns[@]}"; do
        local name
        name=$(ssh_cmd "docker ps --format '{{.Names}}' 2>/dev/null | grep -E '(^|_)${pat}(_|$|-[0-9]+)$' | head -1" 2>/dev/null || true)
        if [[ -n "${name}" ]]; then
            echo "${name}"
            return 0
        fi
    done
    return 1
}

# --- Verification Checks ---
check_running() {
    local container="$1" service="$2"
    local status
    status=$(ssh_cmd "docker inspect --format='{{.State.Status}}' '${container}' 2>/dev/null" 2>/dev/null || echo "not_found")
    if [[ "${status}" == "running" ]]; then
        pass "${service}" "container running"
    else
        fail "${service}" "container status: ${status}"
    fi
}

check_health() {
    local container="$1" service="$2"
    local health
    health=$(ssh_cmd "docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' '${container}' 2>/dev/null" 2>/dev/null || echo "unknown")
    case "${health}" in
        healthy)
            pass "${service}" "healthcheck passing"
            ;;
        unhealthy)
            fail "${service}" "healthcheck unhealthy"
            ;;
        starting)
            warn "${service}" "healthcheck still starting"
            ;;
        none)
            warn "${service}" "no healthcheck defined"
            ;;
        *)
            warn "${service}" "health status: ${health}"
            ;;
    esac
}

check_shim_livez() {
    local service="$1"
    local response
    response=$(ssh_cmd "curl -sf -o /dev/null -w '%{http_code}' http://localhost:${SHIM_PORT}/livez 2>/dev/null" 2>/dev/null || echo "000")
    if [[ "${response}" == "200" ]]; then
        pass "${service}" "health-shim livez responding (HTTP ${response})"
    elif [[ "${response}" == "000" ]]; then
        warn "${service}" "health-shim not reachable on port ${SHIM_PORT}"
    else
        warn "${service}" "health-shim returned HTTP ${response}"
    fi
}

check_memory() {
    local container="$1" service="$2"
    local stats
    stats=$(ssh_cmd "docker stats --no-stream --format '{{.MemUsage}} ({{.MemPerc}})' '${container}' 2>/dev/null" 2>/dev/null || echo "unavailable")
    if [[ "${stats}" == "unavailable" ]]; then
        warn "${service}" "could not retrieve memory stats"
        return
    fi
    # Extract memory percentage
    local mem_pct
    mem_pct=$(echo "${stats}" | grep -oP '[0-9.]+%' | head -1 | tr -d '%')
    if [[ -n "${mem_pct}" ]]; then
        local int_pct="${mem_pct%%.*}"
        if (( int_pct > 90 )); then
            fail "${service}" "memory critical: ${stats}"
        elif (( int_pct > 70 )); then
            warn "${service}" "memory elevated: ${stats}"
        else
            pass "${service}" "memory nominal: ${stats}"
        fi
    else
        pass "${service}" "memory stats collected: ${stats}"
    fi
}

check_graceful_stop() {
    local container="$1" service="$2"
    local exit_code
    exit_code=$(ssh_cmd "timeout 30 docker stop -t 10 '${container}' 2>/dev/null && docker inspect --format='{{.State.ExitCode}}' '${container}' 2>/dev/null" 2>/dev/null || echo "-1")
    if [[ "${exit_code}" == "0" ]]; then
        pass "${service}" "graceful shutdown (exit 0)"
    elif [[ "${exit_code}" == "-1" ]]; then
        fail "${service}" "shutdown timeout or error"
    else
        warn "${service}" "shutdown exit code: ${exit_code}"
    fi
}

check_restart() {
    local container="$1" service="$2"
    local exit_code
    exit_code=$(ssh_cmd "timeout 30 docker start '${container}' 2>/dev/null && sleep 5 && docker inspect --format='{{.State.Status}}' '${container}' 2>/dev/null" 2>/dev/null || echo "failed")
    if [[ "${exit_code}" == "running" ]]; then
        pass "${service}" "restart succeeded"
    else
        fail "${service}" "restart failed (status: ${exit_code})"
    fi
}

# --- Report Generation ---
generate_report() {
    mkdir -p "${REPORT_DIR}"
    {
        echo "# Runtime Verification Report"
        echo ""
        echo "- **Generated**: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
        echo "- **Target**: ${TRUENAS_USER}@${TRUENAS_HOST}"
        echo "- **Images checked**: ${#CRITICAL_ORDER[@]}"
        echo "- **Pass**: ${PASS_COUNT} | **Fail**: ${FAIL_COUNT} | **Warn**: ${WARN_COUNT}"
        echo ""
        echo "## Results"
        echo ""
        echo "| Status | Service | Check |"
        echo "|--------|---------|-------|"
        for r in "${RESULTS[@]}"; do
            IFS='|' read -r status service detail <<< "${r}"
            local icon
            case "${status}" in
                PASS) icon="PASS" ;;
                FAIL) icon="FAIL" ;;
                WARN) icon="WARN" ;;
            esac
            echo "| ${icon} | ${service} | ${detail} |"
        done
        echo ""
        if (( FAIL_COUNT > 0 )); then
            echo "## Failures"
            echo ""
            for r in "${RESULTS[@]}"; do
                IFS='|' read -r status service detail <<< "${r}"
                if [[ "${status}" == "FAIL" ]]; then
                    echo "- **${service}**: ${detail}"
                fi
            done
            echo ""
        fi
        echo "---"
        echo "*Report generated by scripts/runtime-verify.sh*"
    } > "${REPORT_FILE}"
    log "Report written to ${REPORT_FILE}"
}

# --- Main ---
main() {
    log "=== Evergreen Runtime Verification ==="
    log "Target: ${TRUENAS_USER}@${TRUENAS_HOST}"
    log ""

    # Verify SSH connectivity
    if ! ssh_cmd "docker info >/dev/null 2>&1"; then
        log "ERROR: Cannot reach Docker on ${TRUENAS_HOST}. Aborting."
        exit 1
    fi

    for service in "${CRITICAL_ORDER[@]}"; do
        log "--- ${service} ---"

        container=$(find_container "${service}") || true
        if [[ -z "${container}" ]]; then
            fail "${service}" "no running container found"
            continue
        fi

        check_running "${container}" "${service}"
        check_health "${container}" "${service}"
        check_shim_livez "${service}"
        check_memory "${container}" "${service}"
        check_graceful_stop "${container}" "${service}"
        check_restart "${container}" "${service}"

        log ""
    done

    log "========================================"
    log "  SUMMARY: Pass=${PASS_COUNT} Fail=${FAIL_COUNT} Warn=${WARN_COUNT}"
    log "========================================"

    generate_report

    if (( FAIL_COUNT > 0 )); then
        exit 1
    fi
}

main "$@"
