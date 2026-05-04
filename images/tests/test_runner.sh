#!/bin/bash
# =============================================================================
# PER-IMAGE TEST RUNNER
# =============================================================================
# Generates and runs per-image test scripts
# Usage: ./test_runner.sh <image_name> [test_type]
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_FRAMEWORK="$SCRIPT_DIR/test_framework.sh"

IMAGE="${1:-}"
TEST_TYPE="${2:-all}"

if [ -z "$IMAGE" ]; then
    echo "Usage: $0 <image_name> [test_type]"
    echo "Example: $0 traefik all"
    echo "Example: $0 redis functional"
    exit 1
fi

# Import test framework
if [ -f "$TEST_FRAMEWORK" ]; then
    # shellcheck source=/dev/null
    source "$TEST_FRAMEWORK"
else
    echo "ERROR: Test framework not found at $TEST_FRAMEWORK"
    exit 1
fi

# Image-specific test configuration
declare -A IMAGE_CONFIGS=(
    # Binary name, health check port, primary port
    ["traefik"]="traefik,8080,80"
    ["nginx"]="nginx,80,80"
    ["haproxy"]="haproxy,80,80"
    ["envoy"]="envoy,9900,80"
    ["caddy"]="caddy,2019,80"
    ["coredns"]="coredns,53,53"
    ["postgres"]="postgres,5432,5432"
    ["postgresql"]="postgres,5432,5432"
    ["mysql"]="mariadbd,3306,3306"
    ["mariadb"]="mariadbd,3306,3306"
    ["redis"]="redis-server,6379,6379"
    ["memcached"]="memcached,11211,11211"
    ["etcd"]="etcd,2379,2379"
    ["consul"]="consul,8500,8500"
    ["vault"]="vault,8200,8200"
    ["prometheus"]="prometheus,9090,9090"
    ["grafana"]="grafana,3000,3000"
    ["loki"]="loki,3100,3100"
    ["thanos"]="thanos,10902,10902"
    ["node-exporter"]="node_exporter,9100,9100"
    ["jenkins"]="jenkins,8080,8080"
    ["argocd"]="argocd,8080,8080"
    ["rabbitmq"]="rabbitmq-server,15672,5672"
    ["nats"]="nats-server,4222,4222"
    ["minio"]="minio,9000,9000"
    ["restic"]="restic,,"
    ["rclone"]="rclone,,"
    ["trivy"]="trivy,,"
    ["syft"]="syft,,"
    ["grype"]="grype,,"
    ["cosign"]="cosign,,"
    ["step-cli"]="step,,"
    ["forgejo"]="gitea,3000,3000"
    ["gitea"]="gitea,3000,3000"
    ["keycloak"]="keycloak,8080,8080"
    ["openldap"]="slapd,389,389"
    ["zitadel"]="zitadel,8080,8080"
    ["flux"]="flux,3030,3030"
    ["tekton"]="tekton,8080,8080"
    ["drone"]="drone,80,80"
)

# Get image config
get_image_config() {
    local img="$1"
    if [[ -v "IMAGE_CONFIGS[$img]" ]]; then
        echo "${IMAGE_CONFIGS[$img]}"
    else
        # Default - try using image name as binary
        echo "$img,,"
    fi
}

# Run tests for specific image
run_image_tests() {
    local img="$1"
    local config
    config=$(get_image_config "$img")
    
    IFS=',' read -r binary health_port primary_port <<< "$config"
    
    export BINARY="$binary"
    export HEALTH_PORT="$health_port"
    export PRIMARY_PORT="$primary_port"
    
    echo "=========================================="
    echo "Testing Image: $img"
    echo "Binary: $binary"
    echo "Health Port: $health_port"
    echo "Primary Port: $primary_port"
    echo "=========================================="
    
    # Ensure image exists locally (pull if needed)
    local full_image="ghcr.io/wyattau/evergreenimageregistry/$img:latest"
    
    if ! docker image inspect "$full_image" &>/dev/null; then
        echo "Pulling image: $full_image"
        docker pull "$full_image" || {
            echo "ERROR: Failed to pull image"
            return 1
        }
    fi
    
    export IMAGE="$full_image"
    
    # Run requested tests
    case "$TEST_TYPE" in
        all)
            run_all_tests
            ;;
        functional)
            test_functional_basic
            test_functional_ports
            test_functional_environment
            ;;
        security)
            test_c001_non_root
            test_c003_no_shell
            test_c004_no_package_manager
            test_c005_no_sudo
            test_c008_no_docker_socket
            ;;
        constraints)
            test_c001_non_root
            test_c002_readonly_filesystem
            test_c003_no_shell
            test_c004_no_package_manager
            test_c010_health_check
            ;;
        *)
            echo "Unknown test type: $TEST_TYPE"
            exit 1
            ;;
    esac
}

run_image_tests "$IMAGE"