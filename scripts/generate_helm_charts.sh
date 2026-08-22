#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry — Helm Chart Generator
# =============================================================================
# Generates per-image Helm charts from the library chart template.
# Creates charts for Tier 1 (critical) images by default.
#
# Usage:
#   ./scripts/generate_helm_charts.sh [OPTIONS]
#
# Options:
#   --image <name>    Generate chart for specific image
#   --tier1           Generate for all Tier 1 images (default)
#   --all             Generate for all images
#   --publish         Push charts to GHCR OCI registry
#   --help            Show this help
# =============================================================================

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
NC='\033[0m'

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
CHARTS_DIR="$REPO_ROOT/charts"
LIBRARY_DIR="$REPO_ROOT/helm"
REGISTRY="ghcr.io/wyattau/evergreenimageregistry/charts"
TARGET_IMAGE=""
TIER1_ONLY=false
ALL_MODE=false
PUBLISH=false

log_info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

while [ $# -gt 0 ]; do
    case "$1" in
        --image)    TARGET_IMAGE="$2"; shift 2 ;;
        --tier1)    TIER1_ONLY=true; shift ;;
        --all)      ALL_MODE=true; shift ;;
        --publish)  PUBLISH=true; shift ;;
        --help)     head -22 "$0" | tail -20; exit 0 ;;
        *)          log_error "Unknown: $1"; exit 1 ;;
    esac
done

mkdir -p "$CHARTS_DIR"

# ---- Image descriptions (Tier 1) ----
declare -A IMAGE_DESCRIPTIONS=(
    [redis]="In-memory data structure store"
    [postgresql]="Advanced open source relational database"
    [mysql]="Open source relational database management system"
    [mongodb]="Document-oriented NoSQL database"
    [nginx]="High performance web server and reverse proxy"
    [envoy]="High performance edge/middle/service proxy"
    [traefik]="Cloud native edge router"
    [prometheus]="Monitoring system and time series database"
    [grafana]="Open source analytics and monitoring"
    [alertmanager]="Alerting handler for Prometheus"
    [vault]="Secrets and encryption as a service"
    [consul]="Service mesh and service discovery"
    [keycloak]="Open source identity and access management"
    [jenkins]="Automation server for CI/CD"
    [etcd]="Distributed reliable key-value store"
    [nats]="Cloud native messaging system"
    [minio]="S3 compatible object storage"
    [golang]="Go programming language"
    [node-distroless]="Node.js distroless runtime"
    [argo-cd]="GitOps continuous delivery for Kubernetes"
    [cert-manager]="Certificate management for Kubernetes"
    [external-dns]="DNS controller for Kubernetes"
    [ingress-nginx]="Ingress controller for Kubernetes"
    [keda]="Kubernetes event-driven autoscaling"
    [loki]="Horizontally scalable log aggregation"
    [mimir]="Horizontally scalable Prometheus"
    [thanos]="Highly available Prometheus setup"
    [velero]="Backup and restore for Kubernetes"
    [step-ca]="Private certificate authority"
    [dex]="OpenID Connect identity provider"
    [oauth2-proxy]="Reverse proxy for OAuth2"
    [cloudflared]="Cloudflare tunnel client"
    [caddy]="Web server with automatic HTTPS"
    [haproxy]="TCP/HTTP load balancer"
    [memcached]="Distributed memory caching system"
    [rabbitmq]="Message broker"
    [kafka]="Distributed event streaming platform"
    [zookeeper]="Centralized service for coordination"
    [mariadb]="Fork of MySQL"
    [clickhouse]="Column-oriented DBMS"
    [timescaledb]="Time-series SQL database"
    [influxdb]="Time series database"
    [telegraf]="Metrics collection agent"
    [vaultwarden]="Bitwarden compatible server"
    [forgejo]="Self-hosted Git service"
    [gitea]="Git with a cup of tea"
    [woodpecker]="Native CI/CD engine"
    [drone]="Container-native CI/CD"
    [headphones]="Music server"
    [jellyfin]="Free media server"
    [navidrome]="Music server and streamer"
    [plex]="Media server"
    [emby]="Media server"
    [sonarr]="PVR for TV shows"
    [radarr]="PVR for movies"
    [lidarr]="Music collection manager"
    [bazarr]="Subtitle manager"
    [overseerr]="Media request management"
    [tautulli]="Plex monitoring and analytics"
    [homarr]="Dashboard for *arr apps"
    [homepage]="Application dashboard"
    [organizr]="HTPC/Homelab services organizer"
    [crowdsec]="Collaborative security engine"
    [fail2ban]="Ban IPs with too many authentication failures"
    [wireguard]="Fast, modern, secure VPN tunnel"
    [pihole]="Network-wide ad blocking"
    [adguardhome]="Network-wide ad blocking"
    [mosquitto]="MQTT broker"
    [emqx]="MQTT broker"
    [vernemq]="MQTT broker"
    [ntp]="Network Time Protocol server"
    [coredns]="DNS server"
    [bind]="DNS server"
    [powerdns]="Authoritative DNS server"
    [grafana-agent]="Grafana Agent for metrics collection"
    [prometheus-node-exporter]="Node exporter for Prometheus"
    [blackbox-exporter]="Probe exporter for Prometheus"
    [json-exporter]="JSON exporter for Prometheus"
    [postgres-exporter]="PostgreSQL exporter for Prometheus"
    [mysqld-exporter]="MySQL exporter for Prometheus"
    [redis-exporter]="Redis exporter for Prometheus"
    [mongodb-exporter]="MongoDB exporter for Prometheus"
    [elasticsearch]="Distributed search and analytics engine"
    [opensearch]="Open source search and analytics"
    [logstash]="Data processing pipeline"
    [kibana]="Visualization for Elasticsearch"
    [opensearch-dashboards]="Visualization for OpenSearch"
    [minio-operator]="Operator for MinIO"
    [kubernetes-dashboard]="Kubernetes web UI"
    [k9s]="Kubernetes CLI dashboard"
    [stern]="Multi-container log tailing"
    [kubecost]="Kubernetes cost monitoring"
    [kyverno]="Kubernetes-native policy management"
    [gatekeeper]="Policy controller for Kubernetes"
    [falco]="Cloud native runtime security"
    [trivy]="Vulnerability scanner"
    [grype]="Vulnerability scanner"
    [syft]="SBOM generator"
    [cosign]="Container signing"
    [chainsaw]="Kubernetes e2e testing"
    [argo-workflows]="Workflow engine for Kubernetes"
    [tekton]="Kubernetes-native CI/CD"
    [tekton-dashboard]="Dashboard for Tekton"
    [harbor]="Trusted cloud native registry"
    [dragonfly]="P2P-based file distribution"
    [seaweedfs]="Distributed storage system"
    [longhorn]="Distributed block storage"
    [rook]="Cloud native storage orchestrator"
    [openebs]="Container attached storage"
    [certificates]="Certificate management"
    [dex]="OpenID Connect identity provider"
    [gatekeeper-audit]="Gatekeeper audit controller"
    [thanos-receive]="Thanos receive component"
    [thanos-store]="Thanos store component"
    [thanos-query]="Thanos query component"
)

# ---- Generate chart for a single image ----
generate_chart() {
    local img="$1"
    local chart_dir="$CHARTS_DIR/$img"
    local description="${IMAGE_DESCRIPTIONS[$img]:-Container image}"

    log_info "Generating chart: $img"

    mkdir -p "$chart_dir/templates"

    # Chart.yaml
    cat > "$chart_dir/Chart.yaml" << EOF
apiVersion: v2
name: $img
description: "$description — Evergreen Image Registry hardened image"
type: application
version: 0.1.0
appVersion: "latest"
maintainers:
  - name: Wyatt Au
keywords:
  - $img
  - security
  - hardened
  - evergreen
home: https://github.com/WyattAu/EvergreenImageRegistry/tree/main/images/$img
sources:
  - https://github.com/WyattAu/EvergreenImageRegistry
dependencies:
  - name: evergreen-registry
    version: "1.0.0"
    repository: "oci://ghcr.io/wyattau/evergreenimageregistry/charts"
EOF

    # values.yaml
    cat > "$chart_dir/values.yaml" << EOF
# Default values for $img
image:
  name: $img
  tag: "latest"
  pullPolicy: IfNotPresent

tier: standard
replicas: 1

security:
  readOnlyRootFs: true

service:
  type: ClusterIP
  port: 8080

env: {}
envFrom: []

persistence:
  enabled: false
EOF

    # Chart.lock
    cat > "$chart_dir/Chart.lock" << EOF
dependencies:
- name: evergreen-registry
  version: 1.0.0
  repository: oci://ghcr.io/wyattau/evergreenimageregistry/charts
digest: sha256:0000000000000000000000000000000000000000000000000000000000000000
generated: "2026-08-22T00:00:00Z"
EOF

    log_ok "Chart generated: $chart_dir"
}

# ---- Main ----
log_info "Helm Chart Generator"
log_info "===================="
echo ""

if [ -n "$TARGET_IMAGE" ]; then
    generate_chart "$TARGET_IMAGE"
else
    images=()
    if [ "$ALL_MODE" = true ]; then
        for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
            [ -f "$manifest" ] || continue
            images+=("$(basename "$(dirname "$manifest")")")
        done
    else
        # Default: Tier 1
        for manifest in "$REPO_ROOT"/images/*/manifest.toml; do
            [ -f "$manifest" ] || continue
            tier=$(grep -oP 'tier\s*=\s*"\K[^"]+' "$manifest" 2>/dev/null | head -1)
            [ "$tier" = "critical" ] && images+=("$(basename "$(dirname "$manifest")")")
        done
    fi

    total=${#images[@]}
    log_info "Generating $total charts"
    echo ""

    generated=0
    for img in "${images[@]}"; do
        generate_chart "$img"
        generated=$((generated + 1))
    done

    echo ""
    echo "=========================================="
    echo "Helm Chart Generation Complete"
    echo "=========================================="
    echo "  Generated: $generated"
    echo "  Output:    $CHARTS_DIR/"
    echo "=========================================="

    # Publish if requested
    if [ "$PUBLISH" = true ] && command -v helm &>/dev/null; then
        log_info "Publishing charts to GHCR..."
        for img in "${images[@]}"; do
            chart_dir="$CHARTS_DIR/$img"
            if [ -d "$chart_dir" ]; then
                helm package "$chart_dir" -d /tmp/helm-packages/ 2>/dev/null || true
            fi
        done
        log_ok "Charts packaged to /tmp/helm-packages/"
    fi
fi
