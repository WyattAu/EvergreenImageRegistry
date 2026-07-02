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
    [sqlite]="database"
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
        webserver)  echo "evergreen-webserver" ;;
        database)   echo "evergreen-database" ;;
        monitoring) echo "evergreen-default" ;;
        security)   echo "evergreen-security" ;;
        *)          echo "evergreen-default" ;;
    esac
}

get_category_for_image() {
    local image="$1"
    echo "${CATEGORY_MAP[$image]:-default}"
}

check_apparmor_available() {
    if [ ! -d "/etc/apparmor.d" ]; then
        log_error "AppArmor profiles directory /etc/apparmor.d not found"
        log_error "AppArmor may not be installed or enabled on this system"
        return 1
    fi

    if ! command -v apparmor_parser &>/dev/null; then
        log_error "apparmor_parser not found - install apparmor-utils"
        return 1
    fi

    if ! command -v aa-status &>/dev/null && ! command -v apparmor_status &>/dev/null; then
        log_warn "aa-status/apparmor_status not found - cannot verify AppArmor is loaded"
    fi

    return 0
}

validate_profile_syntax() {
    local profile="$1"
    if [ ! -f "$profile" ]; then
        log_error "Profile not found: $profile"
        return 1
    fi

    local _check_output
    _check_output=$(apparmor_parser -R "$profile" 2>&1) || true
    local syntax_check
    syntax_check=$(apparmor_parser --skip-cache -p "$profile" 2>&1) || {
        log_error "Syntax error in $profile: $syntax_check"
        return 1
    }

    log_info "  VALID: $(basename "$profile")"
    return 0
}

load_profile() {
    local profile="$1"
    local profile_name
    profile_name=$(basename "$profile" .conf)

    log_step "Loading AppArmor profile: $profile_name"

    if apparmor_parser -r "$profile" 2>&1; then
        log_info "Profile loaded: $profile_name"
        return 0
    else
        log_error "Failed to load profile: $profile_name"
        return 1
    fi
}

unload_profile() {
    local profile="$1"
    local profile_name
    profile_name=$(basename "$profile" .conf)

    if [ "$profile_name" = "apparmor-default" ]; then
        profile_name="evergreen-default"
    fi

    log_step "Unloading AppArmor profile: $profile_name"
    apparmor_parser -R "$profile" 2>/dev/null || true
}

test_image_apparmor() {
    local image="$1"
    local profile_name="$2"
    local profile_file="$3"
    local container_name
    container_name="aa-test-$image-$(date +%s)"
    local full_image="ghcr.io/wyattau/evergreenimageregistry/$image:latest"
    local start_timeout="${START_TIMEOUT:-30}"
    local log_file
    log_file="/tmp/apparmor-test-${image}-$(date +%s).log"

    log_step "Testing image: $full_image"
    log_step "AppArmor profile: $profile_name"

    if ! docker image inspect "$full_image" &>/dev/null; then
        log_info "Pulling image: $full_image"
        docker pull "$full_image" || {
            log_error "Failed to pull image $full_image"
            return 1
        }
    fi

    log_step "Loading AppArmor profile..."
    if ! load_profile "$profile_file"; then
        log_error "Cannot load AppArmor profile - skipping test"
        return 1
    fi

    log_step "Running container with AppArmor profile..."
    docker run --rm \
        --name "$container_name" \
        --security-opt "apparmor=$profile_name" \
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

    local exit_code=0
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

    local run_result=0
    if [ "$exit_code" -eq 0 ] || [ "$exit_code" -eq 137 ]; then
        log_info "Container ran successfully under AppArmor profile"
        run_result=0
    elif [ "$exit_code" -eq 1 ]; then
        log_warn "Container exited with code 1 - may indicate AppArmor denial"
        run_result=1
    else
        log_warn "Container exited with code $exit_code"
        run_result=0
    fi

    if [ -f "$log_file" ]; then
        if grep -qi "apparmor\|denied\|permission denied" "$log_file" 2>/dev/null; then
            log_warn "AppArmor denials detected in container log:"
            grep -iE "apparmor|denied|permission denied" "$log_file" | head -10 || true
        fi

        if [ "${VERBOSE:-false}" = "true" ]; then
            log_info "Full container log:"
            cat "$log_file"
        fi
    fi

    if command -v dmesg &>/dev/null; then
        local aa_denials
        aa_denials=$(dmesg 2>/dev/null | grep -i "apparmor" | grep -i "denied" | tail -20 || true)
        if [ -n "$aa_denials" ]; then
            log_info "Kernel AppArmor denial log entries:"
            echo "$aa_denials" | tail -20
        fi
    fi

    if command -v journalctl &>/dev/null; then
        local journal_denials
        journal_denials=$(journalctl --since "2 minutes ago" -k --no-pager 2>/dev/null | grep -i "apparmor.*denied" | tail -20 || true)
        if [ -n "$journal_denials" ]; then
            log_info "Journal AppArmor denial log entries:"
            echo "$journal_denials"
        fi
    fi

    log_step "Unloading AppArmor profile..."
    unload_profile "$profile_file"

    if [ "${SAVE_LOGS:-false}" = "true" ]; then
        log_info "Log saved to: $log_file"
    else
        rm -f "$log_file"
    fi

    return $run_result
}

test_all_profiles_syntax() {
    log_step "Validating all AppArmor profile syntax..."
    local failed=0
    local total=0

    for profile in "$PROFILES_DIR"/apparmor-*.conf "$PROFILES_DIR"/apparmor-default; do
        [ -f "$profile" ] || continue
        total=$((total + 1))
        if validate_profile_syntax "$profile"; then
            :
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
    echo "  --validate-only   Only validate profile syntax, don't run containers"
    echo "  --verbose         Enable verbose output and save logs"
    echo "  --save-logs       Save container logs to /tmp/"
    echo "  --timeout <secs>  Container start timeout in seconds (default: 30)"
    echo "  --list            List all images and their categories"
    echo ""
    echo "Requirements:"
    echo "  - AppArmor must be installed and enabled"
    echo "  - apparmor_parser must be available"
    echo "  - Docker must support --security-opt apparmor=..."
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
        check_apparmor_available || exit 1
        test_all_profiles_syntax
        exit $?
    fi

    if [ -z "$image" ]; then
        print_usage
        exit 1
    fi

    if ! check_apparmor_available; then
        log_error "AppArmor prerequisites not met"
        exit 1
    fi

    local category
    category=$(get_category_for_image "$image")
    local profile_name
    profile_name=$(get_profile_for_image "$image")
    local profile_file

    case "$category" in
        webserver)  profile_file="$PROFILES_DIR/apparmor-webserver.conf" ;;
        database)   profile_file="$PROFILES_DIR/apparmor-database.conf" ;;
        security)   profile_file="$PROFILES_DIR/apparmor-security.conf" ;;
        *)          profile_file="$PROFILES_DIR/apparmor-default" ;;
    esac

    if [ ! -f "$profile_file" ]; then
        log_error "AppArmor profile not found: $profile_file"
        exit 1
    fi

    if ! validate_profile_syntax "$profile_file"; then
        log_error "Profile validation failed, aborting test"
        exit 1
    fi

    echo ""
    echo "=========================================="
    echo "APPARMOR COMPLIANCE TEST"
    echo "=========================================="
    echo "Image:            $image"
    echo "Category:         $category"
    echo "Profile:          $profile_name"
    echo "Profile file:     $(basename "$profile_file")"
    echo "=========================================="
    echo ""

    local result=0
    if test_image_apparmor "$image" "$profile_name" "$profile_file"; then
        echo ""
        log_info "RESULT: PASS - Image $image is compliant with $profile_name"
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
    echo "Category:         $category"
    echo "AppArmor Profile: $profile_name"
    echo "No-new-privs:     enabled"
    echo "Cap-drop:         ALL"
    echo "Result:           $([ $result -eq 0 ] && echo "COMPLIANT" || echo "NON-COMPLIANT")"
    echo "=========================================="

    exit $result
}

main "$@"
