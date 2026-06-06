#!/usr/bin/env bash
# =============================================================================
# Shim Functionality Test Script
# Builds 5 critical images locally, starts containers, and validates shim
# health checks and metrics endpoints.
# =============================================================================
set -euo pipefail

REGISTRY="ghcr.io/wyattau/evergreenimageregistry"
SHIM_PORT=9101
STARTUP_WAIT=10
CONTAINER_NAME_PREFIX="evergreen-test"

IMAGES=(
  "nginx:80"
  "redis:6379"
  "postgres:5432"
  "grafana:3000"
  "vault:8200"
)

RESULTS=()
CONTAINERS=()

log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
pass() { RESULTS+=("PASS: $1"); log "PASS $1"; }
fail() { RESULTS+=("FAIL: $1 — $2"); log "FAIL $1 — $2"; }

cleanup() {
  log "Cleaning up containers..."
  for c in "${CONTAINERS[@]}"; do
    docker rm -f "$c" >/dev/null 2>&1 || true
  done
}
trap cleanup EXIT

log "=== Evergreen Shim Functionality Tests ==="
log ""

for entry in "${IMAGES[@]}"; do
  IFS=':' read -r img port <<< "$entry"
  tag="${img}"
  container="${CONTAINER_NAME_PREFIX}-${img}"
  image="${REGISTRY}/${img}:latest"

  log "--- Testing ${img} (port ${port}) ---"

  # Step 1: Build image locally
  log "Building ${img}..."
  if ! docker build -t "${image}" "images/${img}/" 2>&1 | tail -1; then
    fail "${img}" "build failed"
    continue
  fi
  log "Build complete."

  # Step 2: Start container
  log "Starting container..."
  docker rm -f "${container}" >/dev/null 2>&1 || true
  if ! docker run -d --name "${container}" -p "${port}:${port}" -p "${SHIM_PORT}:${SHIM_PORT}" "${image}" >/dev/null 2>&1; then
    fail "${img}" "docker run failed"
    continue
  fi
  CONTAINERS+=("${container}")

  # Step 3: Wait for startup
  log "Waiting ${STARTUP_WAIT}s for startup..."
  sleep "${STARTUP_WAIT}"

  # Check container is still running
  if ! docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
    fail "${img}" "container exited unexpectedly"
    docker logs "${container}" 2>&1 | tail -5 || true
    continue
  fi

  # Step 4: Test health check via shim
  log "Testing healthcheck --tcp 127.0.0.1:${port}..."
  if docker exec "${container}" /shim healthcheck --tcp "127.0.0.1:${port}" >/dev/null 2>&1; then
    pass "${img}:healthcheck"
  elif docker exec "${container}" /usr/local/bin/shim healthcheck --tcp "127.0.0.1:${port}" >/dev/null 2>&1; then
    pass "${img}:healthcheck"
  else
    fail "${img}:healthcheck" "shim healthcheck returned non-zero"
  fi

  # Step 5: Test metrics endpoint
  log "Testing metrics endpoint..."
  metrics_response=$(curl -sf "http://localhost:${SHIM_PORT}/metrics" 2>/dev/null || echo "")
  if [ -n "${metrics_response}" ]; then
    pass "${img}:metrics"
    log "  Metrics response (first 200 chars): ${metrics_response:0:200}"
  else
    fail "${img}:metrics" "curl failed or empty response"
  fi

  # Step 6: Stop container
  log "Stopping container..."
  docker stop "${container}" >/dev/null 2>&1 || true
  log ""
done

# Summary
log "========================================"
log "           TEST RESULTS SUMMARY"
log "========================================"
PASS_COUNT=0
FAIL_COUNT=0
for r in "${RESULTS[@]}"; do
  log "  ${r}"
  if [[ "${r}" == PASS* ]]; then
    ((PASS_COUNT++))
  else
    ((FAIL_COUNT++))
  fi
done
log ""
log "Total: $((PASS_COUNT + FAIL_COUNT)) | Pass: ${PASS_COUNT} | Fail: ${FAIL_COUNT}"
log ""

if [ "${FAIL_COUNT}" -gt 0 ]; then
  exit 1
fi
