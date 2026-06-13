#!/usr/bin/env bash
# =============================================================================
# PERFORMANCE BASELINE - CRITICAL EIR IMAGES
# =============================================================================
# Measures startup time, steady-state memory, CPU usage, and image sizes
# for critical EIR images. Outputs a TOML baseline report.
#
# Usage:
#   ./scripts/performance-baseline.sh [--host HOST] [--user USER] [--output PATH]
#
# Runs locally (not remote) - assumes Docker is available locally for the
# startup/memory/CPU tests. Image size comparison pulls from GHCR.
# =============================================================================
set -euo pipefail

# --- Configuration ---
REGISTRY="ghcr.io/wyattau/evergreenimageregistry"
# UPSTREAM_REGISTRY=""  # Set to compare against upstream (e.g., "docker.io/library")
REPORT_DIR="${REPORT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/.reports}"
TIMESTAMP=$(date -u '+%Y%m%dT%H%M%SZ')
REPORT_FILE="${REPORT_DIR}/perf-baseline-${TIMESTAMP}.toml"
RUN_PREFIX="eir-perf-test"
STARTUP_TIMEOUT=60

# Critical images with their ports
declare -A IMAGE_PORTS=(
    ["traefik"]="8080"
    ["postgres"]="5432"
    ["redis-7"]="6379"
    ["grafana"]="3000"
    ["keycloak"]="8080"
    ["forgejo"]="3000"
    ["cloudflared"]="7844"
)

IMAGE_ORDER=(traefik postgres redis-7 grafana keycloak forgejo cloudflared)

# --- State ---
declare -A STARTUP_TIMES=()
declare -A MEMORY_USAGE=()
declare -A CPU_USAGE=()
declare -A EIR_SIZES=()

# --- Helpers ---
log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*" >&2; }

cleanup() {
    log "Cleaning up test containers..."
    for img in "${IMAGE_ORDER[@]}"; do
        docker rm -f "${RUN_PREFIX}-${img}" >/dev/null 2>&1 || true
    done
}
trap cleanup EXIT

# Measure time in milliseconds
time_ms() {
    local start end
    start=$(date +%s%N)
    "$@"
    end=$(date +%s%N)
    echo $(( (end - start) / 1000000 ))
}

# Get image size in MB from docker images
get_image_size_mb() {
    local image="$1"
    local size_bytes
    size_bytes=$(docker image inspect "${image}" --format '{{.Size}}' 2>/dev/null || echo "0")
    echo $(( size_bytes / 1024 / 1024 ))
}

# Wait for healthcheck to pass
wait_healthy() {
    local container="$1"
    local timeout="$2"
    local elapsed=0
    while (( elapsed < timeout )); do
        local status
        status=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}running{{end}}' "${container}" 2>/dev/null || echo "not_found")
        if [[ "${status}" == "healthy" || "${status}" == "running" ]]; then
            return 0
        fi
        sleep 1
        ((elapsed++))
    done
    return 1
}

# --- Measurements ---
measure_startup() {
    local img="$1" port="$2"
    local container="${RUN_PREFIX}-${img}"
    local image="${REGISTRY}/${img}:latest"

    log "  Pulling ${image}..."
    if ! docker pull "${image}" >/dev/null 2>&1; then
        log "  SKIP ${img}: pull failed"
        STARTUP_TIMES["${img}"]="-1"
        return
    fi

    docker rm -f "${container}" >/dev/null 2>&1 || true

    log "  Starting ${img} and measuring startup..."
    local start_ns
    start_ns=$(date +%s%N)

    if ! docker run -d --name "${container}" -p "${port}:${port}" -p "9101:9101" "${image}" >/dev/null 2>&1; then
        STARTUP_TIMES["${img}"]="-1"
        return
    fi

    if wait_healthy "${container}" "${STARTUP_TIMEOUT}"; then
        local end_ns
        end_ns=$(date +%s%N)
        local elapsed_ms=$(( (end_ns - start_ns) / 1000000 ))
        STARTUP_TIMES["${img}"]="${elapsed_ms}"
        log "  ${img} started in ${elapsed_ms}ms"
    else
        local end_ns
        end_ns=$(date +%s%N)
        local elapsed_ms=$(( (end_ns - start_ns) / 1000000 ))
        STARTUP_TIMES["${img}"]="-1"
        log "  ${img} failed to become healthy within ${STARTUP_TIMEOUT}s"
    fi
}

measure_memory() {
    local img="$1"
    local container="${RUN_PREFIX}-${img}"

    if ! docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        MEMORY_USAGE["${img}"]="-1"
        return
    fi

    # Collect 5 samples at 1s intervals
    local total_pct=0
    local count=0
    for _ in 1 2 3 4 5; do
        local stats
        stats=$(docker stats --no-stream --format '{{.MemPerc}}' "${container}" 2>/dev/null | tr -d '%' || echo "0")
        if [[ "${stats}" =~ ^[0-9.]+$ ]]; then
            total_pct=$(echo "${total_pct} + ${stats}" | bc 2>/dev/null || echo "${total_pct}")
            ((count++))
        fi
        sleep 1
    done

    if (( count > 0 )); then
        local avg
        avg=$(echo "scale=2; ${total_pct} / ${count}" | bc 2>/dev/null || echo "0")
        MEMORY_USAGE["${img}"]="${avg}"
    else
        MEMORY_USAGE["${img}"]="-1"
    fi
}

measure_cpu() {
    local img="$1"
    local container="${RUN_PREFIX}-${img}"

    if ! docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        CPU_USAGE["${img}"]="-1"
        return
    fi

    local stats
    stats=$(docker stats --no-stream --format '{{.CPUPerc}}' "${container}" 2>/dev/null | tr -d '%' || echo "0")
    if [[ "${stats}" =~ ^[0-9.]+$ ]]; then
        CPU_USAGE["${img}"]="${stats}"
    else
        CPU_USAGE["${img}"]="-1"
    fi
}

measure_sizes() {
    for img in "${IMAGE_ORDER[@]}"; do
        local image="${REGISTRY}/${img}:latest"
        log "  Measuring size for ${img}..."
        docker pull "${image}" >/dev/null 2>&1 || true
        EIR_SIZES["${img}"]=$(get_image_size_mb "${image}")
    done
}

# --- TOML Report ---
generate_report() {
    mkdir -p "${REPORT_DIR}"
    {
        echo "# Performance Baseline Report"
        echo "# Generated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
        echo "# Registry: ${REGISTRY}"
        echo ""

        for img in "${IMAGE_ORDER[@]}"; do
            echo "[[image]]"
            echo "name = \"${img}\""
            echo "registry = \"${REGISTRY}\""
            echo ""

            local startup="${STARTUP_TIMES["${img}"]:-"-1"}"
            echo "[image.startup]"
            echo "time_ms = ${startup}"
            if (( startup > 0 )); then
                if (( startup < 1000 )); then
                    echo "rating = \"excellent\""
                elif (( startup < 5000 )); then
                    echo "rating = \"good\""
                elif (( startup < 15000 )); then
                    echo "rating = \"acceptable\""
                else
                    echo "rating = \"slow\""
                fi
            else
                echo "rating = \"failed\""
            fi
            echo ""

            echo "[image.memory]"
            echo "avg_percent = ${MEMORY_USAGE["${img}"]:-"-1"}"
            echo ""

            echo "[image.cpu]"
            echo "percent = ${CPU_USAGE["${img}"]:-"-1"}"
            echo ""

            echo "[image.size]"
            echo "eir_mb = ${EIR_SIZES["${img}"]:-"-1"}"
            echo ""
        done

        echo "[summary]"
        echo "total_images = ${#IMAGE_ORDER[@]}"
        echo "timestamp = \"${TIMESTAMP}\""
    } > "${REPORT_FILE}"
    log "Report written to ${REPORT_FILE}"
}

# --- Main ---
main() {
    log "=== EIR Performance Baseline ==="
    log ""

    # Ensure Docker is available
    if ! docker info >/dev/null 2>&1; then
        log "ERROR: Docker not available. Aborting."
        exit 1
    fi

    log "--- Phase 1: Image Sizes ---"
    measure_sizes
    log ""

    log "--- Phase 2: Startup Times ---"
    for img in "${IMAGE_ORDER[@]}"; do
        local port="${IMAGE_PORTS["${img}"]}"
        measure_startup "${img}" "${port}"
    done
    log ""

    log "--- Phase 3: Steady-State Memory & CPU ---"
    for img in "${IMAGE_ORDER[@]}"; do
        log "  Sampling ${img}..."
        measure_memory "${img}"
        measure_cpu "${img}"
    done
    log ""

    log "--- Generating Report ---"
    generate_report

    log ""
    log "=== Baseline Complete ==="
}

main "$@"
