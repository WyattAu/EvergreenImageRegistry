#!/usr/bin/env bash
# =============================================================================
# COLLECT BUILD METRICS SCRIPT
# =============================================================================
# Builds 10 critical images with `time docker build`, records build times in
# JSON format, and saves to .specs/06_5_regression/build_times.json
# =============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
METRICS_FILE="${REPO_ROOT}/.specs/06_5_regression/build_times.json"
IMAGES_DIR="${REPO_ROOT}/images"
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

# Top 10 critical images to benchmark
CRITICAL_IMAGES=(
    "nginx"
    "grafana"
    "prometheus"
    "vault"
    "traefik"
    "minio"
    "etcd"
    "consul"
    "caddy"
    "node-exporter"
)

log() { echo "[$(date -u '+%H:%M:%S')] $*"; }

# Ensure metrics directory exists
mkdir -p "$(dirname "${METRICS_FILE}")"

# Load existing metrics if present
if [ -f "${METRICS_FILE}" ]; then
    EXISTING=$(cat "${METRICS_FILE}")
else
    EXISTING='{"version":1,"description":"Build time baselines for performance regression detection","threshold_percent":50,"images":{}}'
fi

# Build and measure each image
log "=== Building 10 critical images for baseline ==="
TOTAL_IMAGES=${#CRITICAL_IMAGES[@]}
CURRENT=0

for image in "${CRITICAL_IMAGES[@]}"; do
    CURRENT=$((CURRENT + 1))
    dockerfile="${IMAGES_DIR}/${image}/Dockerfile"

    if [ ! -f "${dockerfile}" ]; then
        log "[${CURRENT}/${TOTAL_IMAGES}] SKIP ${image}: no Dockerfile"
        continue
    fi

    log "[${CURRENT}/${TOTAL_IMAGES}] Building ${image}..."

    # Build with timing
    START_NS=$(date +%s%N)
    if docker build \
        --quiet \
        --no-cache \
        --platform linux/amd64 \
        -t "evergreen-benchmark-${image}:test" \
        "${IMAGES_DIR}/${image}" \
        > /tmp/build-${image}.log 2>&1; then
        END_NS=$(date +%s%N)
        ELAPSED_MS=$(( (END_NS - START_NS) / 1000000 ))
        log "  Built in ${ELAPSED_MS}ms"

        # Update metrics JSON using python (jq may not be available)
        python3 -c "
import json, sys

metrics_file = '${METRICS_FILE}'
try:
    with open(metrics_file, 'r') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {'version': 1, 'description': 'Build time baselines for performance regression detection', 'threshold_percent': 50, 'images': {}}

data['images']['${image}'] = {
    'build_time_ms': ${ELAPSED_MS},
    'updated': '${TIMESTAMP}',
    'platform': 'linux/amd64'
}

with open(metrics_file, 'w') as f:
    json.dump(data, f, indent=2)
"
    else
        END_NS=$(date +%s%N)
        ELAPSED_MS=$(( (END_NS - START_NS) / 1000000 ))
        log "  FAILED after ${ELAPSED_MS}ms (see /tmp/build-${image}.log)"

        # Record failure
        python3 -c "
import json

metrics_file = '${METRICS_FILE}'
try:
    with open(metrics_file, 'r') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {'version': 1, 'description': 'Build time baselines for performance regression detection', 'threshold_percent': 50, 'images': {}}

data['images']['${image}'] = {
    'build_time_ms': ${ELAPSED_MS},
    'updated': '${TIMESTAMP}',
    'platform': 'linux/amd64',
    'status': 'failed'
}

with open(metrics_file, 'w') as f:
    json.dump(data, f, indent=2)
"
    fi

    # Cleanup test image
    docker rmi "evergreen-benchmark-${image}:test" 2>/dev/null || true
done

log "=== Build metrics saved to ${METRICS_FILE} ==="

# Display summary
python3 -c "
import json

with open('${METRICS_FILE}', 'r') as f:
    data = json.load(f)

print('\n=== Build Time Summary ===')
print(f\"{'Image':<25} {'Time (ms)':<12} {'Status'}\")
print('-' * 50)
for name, info in sorted(data['images'].items()):
    status = info.get('status', 'ok')
    print(f\"{name:<25} {info['build_time_ms']:<12} {status}\")
"

log "Done."
