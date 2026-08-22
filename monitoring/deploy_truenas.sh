#!/usr/bin/env bash
# =============================================================================
# Deploy EIR Monitoring Stack to TrueNAS
# =============================================================================
# Sets up Prometheus, Grafana, Alertmanager, and EIR Metrics Exporter
# on TrueNAS SCALE using Docker Compose.
#
# Usage:
#   sudo ./monitoring/deploy_truenas.sh [--install-metrics] [--with-trivy]
#
# Options:
#   --install-metrics   Install metrics exporter as systemd service
#   --with-trivy        Include Trivy vulnerability scanner
# =============================================================================

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INSTALL_DIR="/opt/evergreen-image-registry"
METRICS_PORT=9120
PROMETHEUS_PORT=9090
GRAFANA_PORT=3030
ALERTMANAGER_PORT=9093

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
log_ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
log_info() { echo -e "${CYAN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_err()  { echo -e "${RED}[ERROR]${NC} $1"; }

INSTALL_METRICS=false
WITH_TRIVY=false

while [ $# -gt 0 ]; do
    case "$1" in
        --install-metrics) INSTALL_METRICS=true; shift ;;
        --with-trivy)      WITH_TRIVY=true; shift ;;
        *)                 log_err "Unknown: $1"; exit 1 ;;
    esac
done

echo "============================================="
echo "  EIR Monitoring Stack Deployment"
echo "============================================="
echo ""

# Check prerequisites
if ! command -v docker &>/dev/null; then
    log_err "Docker not found. Install Docker first."
    exit 1
fi

if ! docker compose version &>/dev/null; then
    log_err "Docker Compose not found."
    exit 1
fi

# Create data directories
log_info "Creating data directories..."
mkdir -p monitoring/data/{prometheus,alertmanager,grafana}

# Create Prometheus config
log_info "Creating Prometheus configuration..."
mkdir -p monitoring/prometheus/targets

cat > monitoring/prometheus/prometheus.yml << 'EOF'
global:
  scrape_interval: 30s
  evaluation_interval: 30s

rule_files:
  - /etc/prometheus/rules/evergreen-alerts.yml

scrape_configs:
  - job_name: 'evergreen-metrics'
    static_configs:
      - targets: ['eir-metrics:9120']
    metrics_path: /metrics

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'grafana'
    static_configs:
      - targets: ['grafana:3000']
EOF

# Create alert rules
mkdir -p monitoring/prometheus/alerts
cat > monitoring/prometheus/alerts/evergreen-alerts.yml << 'EOF'
groups:
  - name: evergreen-compliance
    rules:
      - alert: HighBlockViolations
        expr: eir_validation_block_violations > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High BLOCK violations detected"
          description: "{{ $value }} BLOCK violations found"

      - alert: LowPassRate
        expr: eir_validation_pass_rate < 0.95
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Validation pass rate below 95%"
          description: "Current rate: {{ $value | humanizePercentage }}"

      - alert: SbomCoverageLow
        expr: eir_sbom_coverage_ratio < 0.5
        for: 10m
        labels:
          severity: info
        annotations:
          summary: "SBOM coverage below 50%"
          description: "Current coverage: {{ $value | humanizePercentage }}"

      - alert: MetricsExporterDown
        expr: up{job="evergreen-metrics"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "EIR Metrics Exporter is down"
          description: "Metrics exporter has been unreachable for 2 minutes"
EOF

# Add metrics exporter service to docker-compose
log_info "Adding EIR Metrics Exporter to docker-compose..."
cat > monitoring/docker-compose.yml << 'COMPOSEOF'
# Evergreen Monitoring Stack (updated with EIR Metrics Exporter)

name: evergreen-monitoring

networks:
  monitoring:
    driver: bridge

services:
  prometheus:
    image: ghcr.io/wyattau/evergreenimageregistry/prometheus:latest
    container_name: evergreen-prometheus
    user: '65532:65532'
    restart: unless-stopped
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/data'
      - '--storage.tsdb.retention.time=90d'
      - '--storage.tsdb.retention.size=50GB'
      - '--web.enable-lifecycle'
      - '--web.listen-address=0.0.0.0:9090'
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./prometheus/alerts/evergreen-alerts.yml:/etc/prometheus/rules/evergreen-alerts.yml:ro
      - ./data/prometheus:/data
    ports:
      - '9090:9090'
    networks: [monitoring]

  alertmanager:
    image: ghcr.io/wyattau/evergreenimageregistry/alertmanager:latest
    container_name: evergreen-alertmanager
    user: '65532:65532'
    restart: unless-stopped
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/data'
      - '--web.listen-address=0.0.0.0:9093'
    volumes:
      - ./alertmanager/config.yml:/etc/alertmanager/alertmanager.yml:ro
      - ./data/alertmanager:/data
    ports:
      - '9093:9093'
    networks: [monitoring]

  grafana:
    image: ghcr.io/wyattau/evergreenimageregistry/grafana:latest
    container_name: evergreen-grafana
    user: '65532:65532'
    restart: unless-stopped
    depends_on:
      - prometheus
    environment:
      GF_SECURITY_ADMIN_USER: ${GF_ADMIN_USER:-admin}
      GF_SECURITY_ADMIN_PASSWORD: ${GF_ADMIN_PASSWORD:-evergreen}
      GF_USERS_ALLOW_SIGN_UP: 'false'
      GF_SERVER_HTTP_PORT: '3000'
      GF_PATHS_PROVISIONING: /etc/grafana/provisioning
      GF_PATHS_DATA: /var/lib/grafana
    volumes:
      - ./data/grafana:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
      - ./grafana/dashboards:/var/lib/grafana/dashboards:ro
    ports:
      - '3030:3000'
    networks: [monitoring]

  node-exporter:
    image: prom/node-exporter:latest
    container_name: evergreen-node-exporter
    restart: unless-stopped
    command:
      - '--path.rootfs=/host'
      - '--web.listen-address=0.0.0.0:9100'
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/host:ro,rslave
    pid: host
    ports:
      - '9100:9100'
    networks: [monitoring]

  eir-metrics:
    image: python:3.12-slim
    container_name: evergreen-eir-metrics
    restart: unless-stopped
    working_dir: /app
    command: ['python3', 'export_metrics.py', '--serve', '--port', '9120']
    volumes:
      - ./scripts:/app:ro
      - /opt/evergreen-image-registry/images:/app/images:ro
      - /opt/evergreen-image-registry/compliance:/app/compliance:ro
    ports:
      - '9120:9120'
    networks: [monitoring]
COMPOSEOF

# Copy scripts to install directory
log_info "Installing scripts to ${INSTALL_DIR}..."
mkdir -p "$INSTALL_DIR"
cp scripts/export_metrics.py "$INSTALL_DIR/"
cp -r compliance/ "$INSTALL_DIR/" 2>/dev/null || true

# Install metrics systemd service if requested
if [ "$INSTALL_METRICS" = true ]; then
    log_info "Installing metrics exporter systemd service..."
    bash monitoring/install_metrics_service.sh
fi

# Deploy
log_info "Deploying monitoring stack..."
cd monitoring
docker compose up -d

echo ""
echo "============================================="
echo "  Deployment Complete!"
echo "============================================="
echo ""
echo "Services:"
echo "  Prometheus:     http://localhost:${PROMETHEUS_PORT}"
echo "  Grafana:        http://localhost:${GRAFANA_PORT}"
echo "  Alertmanager:   http://localhost:${ALERTMANAGER_PORT}"
echo "  EIR Metrics:    http://localhost:${METRICS_PORT}/metrics"
echo "  Node Exporter:  http://localhost:9100/metrics"
echo ""
echo "Grafana Login:"
echo "  User:     ${GF_ADMIN_USER:-admin}"
echo "  Password: ${GF_ADMIN_PASSWORD:-evergreen}"
echo ""
echo "Metrics Endpoint:"
echo "  curl http://localhost:${METRICS_PORT}/metrics"
echo ""
echo "Commands:"
echo "  docker compose -f monitoring/docker-compose.yml logs -f  # View logs"
echo "  docker compose -f monitoring/docker-compose.yml ps       # Check status"
echo "  docker compose -f monitoring/docker-compose.yml restart  # Restart all"
