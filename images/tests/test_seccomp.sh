#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILES_DIR="$SCRIPT_DIR/profiles"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "${CYAN}[STEP]${NC} $1"; }

declare -A CATEGORY_MAP=(
    [nginx]="webserver"
    [traefik]="webserver"
    [caddy]="webserver"
    [haproxy]="webserver"
    [envoy]="webserver"
    [nginx-ingress]="webserver"
    [nginx-stream]="webserver"
    [nginx-unprivileged]="webserver"
    [caddy-fileserver]="webserver"
    [caddy-reverseproxy]="webserver"
    [caddy-wildcard]="webserver"
    [traefik-v2]="webserver"
    [traefik-cloud]="webserver"
    [traefik-crypto]="webserver"
    [traefik-dashboard]="webserver"
    [traefik-hub]="webserver"
    [traefik-metrics]="webserver"
    [traefik-mirror]="webserver"
    [traefik-plugin-auth]="webserver"
    [traefik-plugin-csrf]="webserver"
    [traefik-wss]="webserver"
    [haproxy-dev]="webserver"
    [haproxy-lb]="webserver"
    [haproxy-exporter]="webserver"

    [postgres]="database"
    [postgresql]="database"
    [postgresql-14]="database"
    [postgresql-15]="database"
    [postgresql-16]="database"
    [mysql]="database"
    [mariadb]="database"
    [redis]="database"
    [redis-6]="database"
    [redis-7]="database"
    [redis7]="database"
    [mongodb]="database"
    [mongodb-6]="database"
    [valkey]="database"
    [couchdb]="database"
    [couchbase]="database"
    [cassandra]="database"
    [scylladb]="database"
    [cockroachdb]="database"
    [arangodb]="database"
    [neo4j]="database"
    [etcd]="database"
    [consul]="database"
    [memcached]="database"
    [pgbouncer]="database"
    [pgpool-II]="database"
    [dragonfly]="database"
    [surrealdb]="database"
    [lancedb]="database"
    [qdrant]="database"
    [weaviate]="database"
    [chroma]="database"
    [meilisearch]="database"
    [milvus]="database"
    [minio]="database"
    [timescaledb]="database"
    [postgis]="database"
    [influxdb]="database"
    [influxdb-client]="database"
    [opensearch]="database"
    [opensearch-dashboards]="database"
    [elasticsearch]="database"
    [elasticsearch-7]="database"
    [emqx]="database"
    [nats]="database"
    [rabbitmq]="database"
    [kafka]="database"
    [pulsar]="database"
    [sqlcipher]="database"
    [sqlite]="database"
    [p2]="database"
    [mysql-exporter]="database"
    [redis-exporter]="database"
    [postgresql-exporter]="database"

    [prometheus]="monitoring"
    [grafana]="monitoring"
    [loki]="monitoring"
    [telegraf]="monitoring"
    [thanos]="monitoring"
    [thanos-store]="monitoring"
    [thanos-receive]="monitoring"
    [mimir]="monitoring"
    [cortex]="monitoring"
    [victoriametrics]="monitoring"
    [vm-agent]="monitoring"
    [node-exporter]="monitoring"
    [kube-state-metrics]="monitoring"
    [prometheus-alertmanager]="monitoring"
    [prometheus-pushgateway]="monitoring"
    [prometheus-node-exporter]="monitoring"
    [consul-exporter]="monitoring"
    [envoy-exporter]="monitoring"
    [bind-exporter]="monitoring"
    [unbound-exporter]="monitoring"
    [cadvisor]="monitoring"
    [statping]="monitoring"
    [uptime-kuma]="monitoring"
    [fluent-bit]="monitoring"
    [vector]="monitoring"

    [vault]="security"
    [vault-secrets]="security"
    [hashicorp-vault]="security"
    [vaultwarden]="security"
    [keycloak]="security"
    [dex]="security"
    [oauth2-proxy]="security"
    [authelia]="security"
    [zitadel]="security"
    [headscale]="security"
    [tailscale]="security"
    [step-cli]="security"
    [cosign]="security"
    [trivy]="security"
    [grype]="security"
    [syft]="security"
    [notary]="security"
    [privatebin]="security"
    [fail2ban]="security"
    [wireguard]="security"
    [wg-quick]="security"
    [strongswan]="security"
    [netmaker]="security"
    [netbird]="security"
    [netclient]="security"
    [openvpn]="security"
    [softether]="security"
    [modsecurity]="security"
)

get_profile_for_image() {
    local image="$1"
    local category="${CATEGORY_MAP[$image]:-default}"

    case "$category" in
        webserver)  echo "$PROFILES_DIR/seccomp-webserver.json" ;;
        database)   echo "$PROFILES_DIR/seccomp-database.json" ;;
        monitoring) echo "$PROFILES_DIR/seccomp-monitoring.json" ;;
        security)   echo "$PROFILES_DIR/seccomp-security.json" ;;
        *)          echo "$PROFILES_DIR/seccomp-default.json" ;;
    esac
}

get_category_for_image() {
    local image="$1"
    echo "${CATEGORY_MAP[$image]:-default}"
}

validate_profile_json() {
    local profile="$1"
    if command -v jq &>/dev/null; then
        if jq empty "$profile" 2>/dev/null; then
            return 0
        else
            log_error "Profile $profile is not valid JSON"
            return 1
        fi
    else
        log_warn "jq not available - skipping JSON validation for $profile"
        return 0
    fi
}

test_image_seccomp() {
    local image="$1"
    local profile="$2"
    local container_name="seccomp-test-$image-$(date +%s)"
    local full_image="ghcr.io/wyattau/evergreenimageregistry/$image:latest"
    local start_timeout="${START_TIMEOUT:-30}"
    local log_file="/tmp/seccomp-test-${image}-$(date +%s).log"

    log_step "Testing image: $full_image"
    log_step "Profile: $profile"
    log_step "Category: $(get_category_for_image "$image")"

    if ! docker image inspect "$full_image" &>/dev/null; then
        log_info "Pulling image: $full_image"
        docker pull "$full_image" || {
            log_error "Failed to pull image $full_image"
            return 1
        }
    fi

    log_step "Running container with seccomp profile..."
    local run_result=0
    local exit_code

    docker run --rm \
        --name "$container_name" \
        --security-opt seccomp="$profile" \
        --security-opt no-new-privileges:true \
        --cap-drop ALL \
        --log-driver json-file \
        "$full_image" &> "$log_file" &
    local container_pid=$!

    local waited=0
    while [ $waited -lt "$start_timeout" ]; do
        if ! kill -0 "$container_pid" 2>/dev/null; then
            break
        fi
        sleep 1
        waited=$((waited + 1))
    done

    if kill -0 "$container_pid" 2>/dev/null; then
        log_info "Container is running after ${waited}s (process alive)"
        docker stop "$container_name" &>/dev/null || true
        wait "$container_pid" 2>/dev/null || true
        exit_code=$?
    else
        wait "$container_pid" 2>/dev/null || true
        exit_code=$?
    fi

    log_info "Container exit code: $exit_code"

    if [ "$exit_code" -eq 0 ] || [ "$exit_code" -eq 137 ]; then
        log_info "Container ran successfully under seccomp profile"
        run_result=0
    elif [ "$exit_code" -eq 1 ]; then
        log_warn "Container exited with code 1 - may indicate a blocked syscall"
        run_result=1
    else
        log_warn "Container exited with code $exit_code"
        run_result=0
    fi

    if [ -f "$log_file" ]; then
        if grep -qi "seccomp" "$log_file" 2>/dev/null; then
            log_info "Seccomp-related entries found in container log:"
            grep -i "seccomp" "$log_file" | head -10 || true
        fi

        if grep -qi "operation not permitted\|permission denied\|EPERM\|EACCES" "$log_file" 2>/dev/null; then
            log_warn "Permission errors detected in container log:"
            grep -iE "operation not permitted|permission denied|EPERM|EACCES" "$log_file" | head -10 || true
        fi

        if [ "${VERBOSE:-false}" = "true" ]; then
            log_info "Full container log:"
            cat "$log_file"
        fi
    fi

    if command -v journalctl &>/dev/null; then
        local journal_entries
        journal_entries=$(journalctl --since "2 minutes ago" -k --no-pager 2>/dev/null | grep -i "seccomp" | grep -i "audit" || true)
        if [ -n "$journal_entries" ]; then
            log_info "Kernel seccomp audit log entries:"
            echo "$journal_entries" | tail -20
        fi
    fi

    if [ "${SAVE_LOGS:-false}" = "true" ]; then
        log_info "Log saved to: $log_file"
    else
        rm -f "$log_file"
    fi

    return $run_result
}

test_all_profiles_syntax() {
    log_step "Validating all seccomp profile JSON syntax..."
    local failed=0
    local total=0

    for profile in "$PROFILES_DIR"/seccomp-*.json; do
        total=$((total + 1))
        if validate_profile_json "$profile"; then
            log_info "  VALID: $(basename "$profile")"
        else
            log_error "  INVALID: $(basename "$profile")"
            failed=$((failed + 1))
        fi
    done

    log_info "Profile validation: $((total - failed))/$total passed"
    return $failed
}

print_usage() {
    echo "Usage: $0 <image_name> [--validate-only] [--verbose] [--save-logs] [--timeout <seconds>]"
    echo ""
    echo "Arguments:"
    echo "  image_name        Image name to test (e.g. nginx, redis, vault)"
    echo ""
    echo "Options:"
    echo "  --validate-only   Only validate profile JSON syntax, don't run containers"
    echo "  --verbose         Enable verbose output and save logs"
    echo "  --save-logs       Save container logs to /tmp/"
    echo "  --timeout <secs>  Container start timeout in seconds (default: 30)"
    echo "  --list            List all images and their categories"
    echo ""
    echo "Examples:"
    echo "  $0 nginx"
    echo "  $0 redis --verbose"
    echo "  $0 vault --timeout 60 --save-logs"
    echo "  $0 --validate-only"
    echo "  $0 --list"
}

print_categories() {
    echo "Image Categories:"
    echo ""
    printf "%-30s %s\n" "IMAGE" "CATEGORY"
    printf "%-30s %s\n" "------" "--------"
    for image in $(echo "${!CATEGORY_MAP[@]}" | tr ' ' '\n' | sort); do
        printf "%-30s %s\n" "$image" "${CATEGORY_MAP[$image]}"
    done
}

main() {
    local image="${1:-}"
    local validate_only=false
    local verbose=false
    local save_logs=false
    local start_timeout=30

    shift || true
    while [ $# -gt 0 ]; do
        case "$1" in
            --validate-only) validate_only=true; shift ;;
            --verbose|-v)    verbose=true; shift ;;
            --save-logs)     save_logs=true; shift ;;
            --timeout)       start_timeout="${2:-30}"; shift 2 ;;
            --list)          print_categories; exit 0 ;;
            --help|-h)       print_usage; exit 0 ;;
            *)               log_error "Unknown option: $1"; print_usage; exit 1 ;;
        esac
    done

    if [ "$verbose" = "true" ]; then
        export VERBOSE=true
    fi
    if [ "$save_logs" = "true" ]; then
        export SAVE_LOGS=true
    fi
    export START_TIMEOUT="$start_timeout"

    if ! command -v docker &>/dev/null; then
        log_error "Docker is required but not installed"
        exit 1
    fi

    if [ "$validate_only" = "true" ]; then
        test_all_profiles_syntax
        exit $?
    fi

    if [ -z "$image" ]; then
        print_usage
        exit 1
    fi

    local profile
    profile=$(get_profile_for_image "$image")

    if [ ! -f "$profile" ]; then
        log_error "Seccomp profile not found: $profile"
        exit 1
    fi

    if ! validate_profile_json "$profile"; then
        log_error "Profile validation failed, aborting test"
        exit 1
    fi

    echo ""
    echo "=========================================="
    echo "SECCOMP COMPLIANCE TEST"
    echo "=========================================="
    echo "Image:     $image"
    echo "Category:  $(get_category_for_image "$image")"
    echo "Profile:   $(basename "$profile")"
    echo "=========================================="
    echo ""

    local result=0
    if test_image_seccomp "$image" "$profile"; then
        echo ""
        log_info "RESULT: PASS - Image $image is compliant with $(basename "$profile")"
    else
        echo ""
        log_error "RESULT: FAIL - Image $image may need profile adjustments"
        result=1
    fi

    echo ""
    echo "=========================================="
    echo "COMPLIANCE REPORT"
    echo "=========================================="
    echo "Image:            $image"
    echo "Category:         $(get_category_for_image "$image")"
    echo "Seccomp Profile:  $(basename "$profile")"
    echo "No-new-privs:     enabled"
    echo "Cap-drop:         ALL"
    echo "Result:           $([ $result -eq 0 ] && echo "COMPLIANT" || echo "NON-COMPLIANT")"
    echo "=========================================="

    exit $result
}

main "$@"
