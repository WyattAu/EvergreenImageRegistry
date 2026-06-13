#!/usr/bin/env bash
# ============================================================================
# Evergreen Monitoring Stack - TrueNAS Deployment Script
# ----------------------------------------------------------------------------
# Deploys the Evergreen monitoring stack (Prometheus, AlertManager, Grafana,
# Node Exporter) to a remote TrueNAS server over SSH.
#
# This script does NOT SSH interactively. It copies the monitoring config tree
# to the TrueNAS host, brings the stack up with docker compose, and verifies
# each service is healthy via its HTTP health endpoint.
#
# Usage:
#   ./monitoring/deploy.sh                    # deploy using defaults
#   REMOTE_USER=ops REMOTE_HOST=10.0.0.5 ./monitoring/deploy.sh
#
# Defaults:  wyatt@192.168.1.3 -> /mnt/pool_HDD_x2/infra/monitoring/
# ============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration (overridable via environment)
# ---------------------------------------------------------------------------
REMOTE_USER="${REMOTE_USER:-wyatt}"
REMOTE_HOST="${REMOTE_HOST:-192.168.1.3}"
REMOTE_DIR="${REMOTE_DIR:-/mnt/pool_HDD_x2/infra/monitoring}"
DATA_UID="${DATA_UID:-65532}"   # Evergreen non-root UID
COMPOSE_FILE="docker-compose.yml"

# Local source directory (the monitoring/ folder this script lives in)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="${SCRIPT_DIR}"

REMOTE="${REMOTE_USER}@${REMOTE_HOST}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
log()  { printf '\033[1;34m[deploy]\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m  OK\033[0m  %s\n' "$*"; }
warn() { printf '\033[1;33m WARN\033[0m  %s\n' "$*"; }
die()  { printf '\033[1;31m FAIL\033[0m %s\n' "$*" >&2; exit 1; }

# Resolve which docker compose command the remote host supports.
remote_compose_cmd() {
  ssh "${SSH_OPTS[@]}" "${REMOTE}" \
    'command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1 && echo "docker compose" && exit 0;
     command -v docker-compose >/dev/null 2>&1 && echo "docker-compose" && exit 0;
     exit 1'
}

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
log "Pre-flight checks"

command -v rsync >/dev/null 2>&1 || die "rsync not found on local machine. Install it first."
command -v ssh    >/dev/null 2>&1 || die "ssh not found on local machine."

SSH_OPTS=(-o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=accept-new)

ssh "${SSH_OPTS[@]}" "${REMOTE}" 'echo ok' >/dev/null 2>&1 \
  || die "Cannot reach ${REMOTE}. Ensure SSH key auth is configured."

[ -f "${SRC_DIR}/${COMPOSE_FILE}" ]       || die "Missing ${SRC_DIR}/${COMPOSE_FILE}"
[ -f "${SRC_DIR}/prometheus/prometheus.yml" ] || die "Missing prometheus/prometheus.yml"

ok "SSH to ${REMOTE} works"
ok "Required local files present"

# ---------------------------------------------------------------------------
# 1. Sync monitoring configs to TrueNAS
# ---------------------------------------------------------------------------
log "Syncing monitoring configs -> ${REMOTE}:${REMOTE_DIR}/"

ssh "${SSH_OPTS[@]}" "${REMOTE}" "mkdir -p '${REMOTE_DIR}/prometheus/targets' \
                                             '${REMOTE_DIR}/prometheus/alerts' \
                                             '${REMOTE_DIR}/alertmanager' \
                                             '${REMOTE_DIR}/grafana/dashboards' \
                                             '${REMOTE_DIR}/grafana/provisioning/datasources' \
                                             '${REMOTE_DIR}/grafana/provisioning/dashboards'"

# rsync the whole tree (config only; exclude any local data/runtime artefacts).
rsync -avz --delete \
  --exclude 'data/' \
  --exclude '*.log' \
  --exclude '.git/' \
  -e "ssh ${SSH_OPTS[*]}" \
  "${SRC_DIR}/" "${REMOTE}:${REMOTE_DIR}/"

ok "Configs synced"

# ---------------------------------------------------------------------------
# 2. Ensure data directories + correct ownership (UID 65532)
# ---------------------------------------------------------------------------
log "Preparing persistent data directories"

ssh "${SSH_OPTS[@]}" "${REMOTE}" bash -s <<REMOTE_PREP
set -euo pipefail
mkdir -p "${REMOTE_DIR}/data/prometheus" \
         "${REMOTE_DIR}/data/grafana" \
         "${REMOTE_DIR}/data/alertmanager"
# Evergreen images run as non-root UID ${DATA_UID}; grant write access.
sudo chown -R ${DATA_UID}:${DATA_UID} "${REMOTE_DIR}/data" 2>/dev/null \
  || chown -R ${DATA_UID}:${DATA_UID} "${REMOTE_DIR}/data"
echo "data-dirs-ready"
REMOTE_PREP

ok "Data directories owned by UID ${DATA_UID}"

# ---------------------------------------------------------------------------
# 3. Pull images and bring the stack up
# ---------------------------------------------------------------------------
log "Pulling Evergreen images on ${REMOTE_HOST}"

COMPOSE_CMD="$(remote_compose_cmd)" \
  || die "Neither 'docker compose' nor 'docker-compose' found on ${REMOTE}."
ok "Compose command: ${COMPOSE_CMD}"

ssh "${SSH_OPTS[@]}" "${REMOTE}" \
  "cd '${REMOTE_DIR}' && ${COMPOSE_CMD} pull"

log "Starting monitoring stack"
ssh "${SSH_OPTS[@]}" "${REMOTE}" \
  "cd '${REMOTE_DIR}' && ${COMPOSE_CMD} up -d"

ok "Stack started"

# ---------------------------------------------------------------------------
# 4. Verify services are healthy
# ---------------------------------------------------------------------------
log "Waiting for services to become healthy (up to 120s)"

check_endpoint() {
  local name="$1" url="$2" expect="$3"
  local elapsed=0
  while [ "${elapsed}" -lt 120 ]; do
    if ssh "${SSH_OPTS[@]}" "${REMOTE}" \
         "curl -fsS -o /dev/null '${url}' 2>/dev/null" \
         && ssh "${SSH_OPTS[@]}" "${REMOTE}" \
              "curl -fsS '${url}' 2>/dev/null | grep -q '${expect}'"; then
      ok "${name} healthy (${url})"
      return 0
    fi
    sleep 5
    elapsed=$((elapsed + 5))
  done
  warn "${name} did not become healthy within 120s (${url})"
  return 1
}

# Prometheus  -> /-/healthy returns "Prometheus Server is Healthy."
# AlertManager-> /-/healthy returns body containing "OK"
# Grafana     -> /api/health returns JSON with "database":"ok"
check_endpoint "prometheus"    "http://localhost:9090/-/healthy" "Healthy"
check_endpoint "alertmanager"  "http://localhost:9093/-/healthy" "OK"      || true
check_endpoint "grafana"       "http://localhost:3000/api/health" '"ok"'   || true

# Node exporter has no dedicated health path; verify the metrics endpoint serves.
if ssh "${SSH_OPTS[@]}" "${REMOTE}" \
     "curl -fsS 'http://localhost:9100/metrics' 2>/dev/null | grep -q 'node_'" ; then
  ok "node-exporter healthy (http://localhost:9100/metrics)"
else
  warn "node-exporter metrics not available on :9100 yet"
fi

# ---------------------------------------------------------------------------
# 5. Summary
# ---------------------------------------------------------------------------
log "Container status on ${REMOTE_HOST}:"
ssh "${SSH_OPTS[@]}" "${REMOTE}" \
  "cd '${REMOTE_DIR}' && ${COMPOSE_CMD} ps"

echo
ok "Deployment complete."
printf '\n\033[1;36mAccess points:\033[0m\n'
printf '  Prometheus : http://%s:9090\n' "${REMOTE_HOST}"
printf '  AlertManager: http://%s:9093\n' "${REMOTE_HOST}"
printf '  Grafana    : http://%s:3000  (admin / ${GF_ADMIN_PASSWORD:-evergreen})\n' "${REMOTE_HOST}"
printf '  Node Exporter: http://%s:9100/metrics\n' "${REMOTE_HOST}"
