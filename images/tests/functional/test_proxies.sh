#!/bin/bash
# =============================================================================
# FUNCTIONAL TEST SUITE - PROXIES / LOAD BALANCERS
# =============================================================================
# Tests for proxy images: Nginx, Traefik, HAProxy, Caddy, Envoy
#
# Usage: IMAGE=<image> ./test_proxies.sh
#        ./test_proxies.sh <image>
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

IMAGE="${IMAGE:-${1:-}}"
CONTAINER_NAME=""
PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0
TOTAL=0

cleanup() {
    if [ -n "$CONTAINER_NAME" ]; then
        docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
        docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    fi
}
trap cleanup EXIT

record() {
    local test_id="$1" status="$2" desc="$3"
    TOTAL=$((TOTAL + 1))
    case "$status" in
        PASS) PASS_COUNT=$((PASS_COUNT + 1)); echo -e "  ${GREEN}PASS${NC} [$test_id] $desc" ;;
        FAIL) FAIL_COUNT=$((FAIL_COUNT + 1)); echo -e "  ${RED}FAIL${NC} [$test_id] $desc" ;;
        SKIP) SKIP_COUNT=$((SKIP_COUNT + 1)); echo -e "  ${YELLOW}SKIP${NC} [$test_id] $desc" ;;
    esac
}

wait_for_port() {
    local port="$1" max_wait="${2:-30}"
    local waited=0
    while [ $waited -lt $max_wait ]; do
        if ! docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
            return 1
        fi
        if command -v nc &>/dev/null; then
            if nc -z 127.0.0.1 "$port" 2>/dev/null; then
                return 0
            fi
        elif command -v curl &>/dev/null; then
            if curl -sf --max-time 1 "http://127.0.0.1:$port/" >/dev/null 2>&1; then
                return 0
            fi
        fi
        sleep 2
        waited=$((waited + 2))
    done
    return 1
}

wait_for_container() {
    local max_wait="${1:-30}"
    local waited=0
    while [ $waited -lt $max_wait ]; do
        if ! docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
            return 1
        fi
        local health
        health=$(docker inspect --format='{{.State.Health.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "unknown")
        if [ "$health" = "healthy" ]; then
            return 0
        fi
        sleep 2
        waited=$((waited + 2))
    done
    docker ps -q -f name="$CONTAINER_NAME" | grep -q .
}

detect_proxy_type() {
    local img="$1"
    case "$img" in
        *nginx*) echo "nginx" ;;
        *traefik*) echo "traefik" ;;
        *haproxy*) echo "haproxy" ;;
        *caddy*) echo "caddy" ;;
        *envoy*) echo "envoy" ;;
        *apache*|*httpd*) echo "apache" ;;
        *oauth2-proxy*) echo "oauth2-proxy" ;;
        *modsecurity*) echo "modsecurity" ;;
        *) echo "unknown" ;;
    esac
}

# =============================================================================
# NGINX TESTS
# =============================================================================

test_nginx() {
    echo ""
    echo "--- Nginx Tests ---"

    CONTAINER_NAME="proxytest-nginx-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -p 18080:80 \
        "$IMAGE" >/dev/null 2>&1; then
        record "NGINX-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_port 18080 15; then
        record "NGINX-START" "FAIL" "Container did not become ready on port 80"
        docker logs "$CONTAINER_NAME" 2>&1 | tail -5
        return
    fi
    record "NGINX-START" "PASS" "Container started and listening on port 80"

    if command -v curl &>/dev/null; then
        local http_code
        http_code=$(curl -sf -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:18080/" 2>/dev/null || echo "000")
        if [ "$http_code" != "000" ]; then
            record "NGINX-HTTP" "PASS" "HTTP response code: $http_code"
        else
            record "NGINX-HTTP" "FAIL" "No HTTP response received"
        fi

        local headers
        headers=$(curl -sI --max-time 5 "http://127.0.0.1:18080/" 2>/dev/null | head -5 || echo "")
        if echo "$headers" | grep -qi "server:"; then
            record "NGINX-HEADERS" "PASS" "Server header present"
        else
            record "NGINX-HEADERS" "SKIP" "Server header not detected (may be hidden)"
        fi
    else
        record "NGINX-HTTP" "SKIP" "curl not available"
        record "NGINX-HEADERS" "SKIP" "curl not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# TRAEFIK TESTS
# =============================================================================

test_traefik() {
    echo ""
    echo "--- Traefik Tests ---"

    CONTAINER_NAME="proxytest-traefik-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -p 18080:8080 \
        -p 18081:80 \
        "$IMAGE" --api.insecure=true >/dev/null 2>&1; then
        record "TRAEFIK-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_port 18080 20; then
        record "TRAEFIK-START" "FAIL" "Container did not become ready on port 8080"
        docker logs "$CONTAINER_NAME" 2>&1 | tail -5
        return
    fi
    record "TRAEFIK-START" "PASS" "Container started and listening on port 8080"

    if command -v curl &>/dev/null; then
        local http_code
        http_code=$(curl -sf -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:18080/api/overview" 2>/dev/null || echo "000")
        if [ "$http_code" = "200" ]; then
            record "TRAEFIK-DASHBOARD" "PASS" "Dashboard API responds with 200"
        elif [ "$http_code" != "000" ]; then
            record "TRAEFIK-DASHBOARD" "SKIP" "Dashboard API responded with $http_code (may need config)"
        else
            record "TRAEFIK-DASHBOARD" "FAIL" "No response from dashboard API"
        fi
    else
        record "TRAEFIK-DASHBOARD" "SKIP" "curl not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# HAPROXY TESTS
# =============================================================================

test_haproxy() {
    echo ""
    echo "--- HAProxy Tests ---"

    CONTAINER_NAME="proxytest-haproxy-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -p 18080:80 \
        -p 18443:443 \
        "$IMAGE" >/dev/null 2>&1; then
        record "HAPROXY-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_port 18080 15; then
        record "HAPROXY-START" "FAIL" "Container did not become ready on port 80"
        docker logs "$CONTAINER_NAME" 2>&1 | tail -5
        return
    fi
    record "HAPROXY-START" "PASS" "Container started and listening on port 80"

    if command -v curl &>/dev/null; then
        local http_code
        http_code=$(curl -sf -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:18080/" 2>/dev/null || echo "000")
        if [ "$http_code" != "000" ]; then
            record "HAPROXY-HTTP" "PASS" "HTTP response code: $http_code"
        else
            record "HAPROXY-HTTP" "FAIL" "No HTTP response received"
        fi

        local stats_code
        stats_code=$(curl -sf -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:18080/haproxy?stats" 2>/dev/null || echo "000")
        if [ "$stats_code" = "200" ]; then
            record "HAPROXY-STATS" "PASS" "Stats endpoint responds with 200"
        else
            record "HAPROXY-STATS" "SKIP" "Stats endpoint returned $stats_code (may need config)"
        fi
    else
        record "HAPROXY-HTTP" "SKIP" "curl not available"
        record "HAPROXY-STATS" "SKIP" "curl not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# CADDY TESTS
# =============================================================================

test_caddy() {
    echo ""
    echo "--- Caddy Tests ---"

    CONTAINER_NAME="proxytest-caddy-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -p 18080:80 \
        "$IMAGE" >/dev/null 2>&1; then
        record "CADDY-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_port 18080 15; then
        record "CADDY-START" "FAIL" "Container did not become ready on port 80"
        docker logs "$CONTAINER_NAME" 2>&1 | tail -5
        return
    fi
    record "CADDY-START" "PASS" "Container started and listening on port 80"

    if command -v curl &>/dev/null; then
        local http_code
        http_code=$(curl -sf -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:18080/" 2>/dev/null || echo "000")
        if [ "$http_code" != "000" ]; then
            record "CADDY-HTTP" "PASS" "HTTP response code: $http_code"
        else
            record "CADDY-HTTP" "FAIL" "No HTTP response received"
        fi
    else
        record "CADDY-HTTP" "SKIP" "curl not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# ENVOY TESTS
# =============================================================================

test_envoy() {
    echo ""
    echo "--- Envoy Tests ---"

    CONTAINER_NAME="proxytest-envoy-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -p 19000:9900 \
        -p 18080:80 \
        "$IMAGE" >/dev/null 2>&1; then
        record "ENVOY-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_port 19000 20; then
        record "ENVOY-START" "FAIL" "Container did not become ready on admin port 9900"
        docker logs "$CONTAINER_NAME" 2>&1 | tail -5
        return
    fi
    record "ENVOY-START" "PASS" "Container started and listening on admin port 9900"

    if command -v curl &>/dev/null; then
        local http_code
        http_code=$(curl -sf -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:19000/server_info" 2>/dev/null || echo "000")
        if [ "$http_code" = "200" ]; then
            record "ENVOY-ADMIN" "PASS" "Admin interface responds with 200"
        elif [ "$http_code" != "000" ]; then
            record "ENVOY-ADMIN" "SKIP" "Admin interface returned $http_code"
        else
            record "ENVOY-ADMIN" "FAIL" "No response from admin interface"
        fi

        local clusters_code
        clusters_code=$(curl -sf -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:19000/clusters" 2>/dev/null || echo "000")
        if [ "$clusters_code" = "200" ]; then
            record "ENVOY-CLUSTERS" "PASS" "Clusters endpoint responds with 200"
        else
            record "ENVOY-CLUSTERS" "SKIP" "Clusters endpoint returned $clusters_code"
        fi
    else
        record "ENVOY-ADMIN" "SKIP" "curl not available"
        record "ENVOY-CLUSTERS" "SKIP" "curl not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# APACHE TESTS
# =============================================================================

test_apache() {
    echo ""
    echo "--- Apache Tests ---"

    CONTAINER_NAME="proxytest-apache-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -p 18080:80 \
        "$IMAGE" >/dev/null 2>&1; then
        record "APACHE-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_port 18080 15; then
        record "APACHE-START" "FAIL" "Container did not become ready on port 80"
        docker logs "$CONTAINER_NAME" 2>&1 | tail -5
        return
    fi
    record "APACHE-START" "PASS" "Container started and listening on port 80"

    if command -v curl &>/dev/null; then
        local http_code
        http_code=$(curl -sf -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:18080/" 2>/dev/null || echo "000")
        if [ "$http_code" != "000" ]; then
            record "APACHE-HTTP" "PASS" "HTTP response code: $http_code"
        else
            record "APACHE-HTTP" "FAIL" "No HTTP response received"
        fi
    else
        record "APACHE-HTTP" "SKIP" "curl not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# GENERIC PROXY TEST (fallback)
# =============================================================================

test_generic_proxy() {
    echo ""
    echo "--- Generic Proxy Test ---"

    local entrypoint
    entrypoint=$(docker inspect "$IMAGE" --format='{{(index .Config.Entrypoint 0)}}' 2>/dev/null || echo "")
    local exposed_ports
    exposed_ports=$(docker inspect "$IMAGE" --format='{{json .Config.ExposedPorts}}' 2>/dev/null || echo "{}")

    record "GENERIC-START" "SKIP" "No specific test for this image (entrypoint=$entrypoint, ports=$exposed_ports)"

    CONTAINER_NAME="proxytest-generic-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        "$IMAGE" >/dev/null 2>&1; then
        record "GENERIC-RUN" "FAIL" "Container failed to start"
        return
    fi

    if wait_for_container 15; then
        record "GENERIC-RUN" "PASS" "Container started and is running"
    else
        record "GENERIC-RUN" "FAIL" "Container did not become ready"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    if [ -z "$IMAGE" ]; then
        echo "Usage: IMAGE=<image> $0"
        echo "       $0 <image>"
        exit 1
    fi

    if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
        echo "ERROR: Image '$IMAGE' not found locally"
        exit 1
    fi

    echo "=========================================="
    echo "PROXY FUNCTIONAL TESTS"
    echo "Image: $IMAGE"
    echo "=========================================="

    local proxy_type
    proxy_type=$(detect_proxy_type "$IMAGE")
    echo "Detected proxy type: $proxy_type"

    case "$proxy_type" in
        nginx) test_nginx ;;
        traefik) test_traefik ;;
        haproxy) test_haproxy ;;
        caddy) test_caddy ;;
        envoy) test_envoy ;;
        apache) test_apache ;;
        *) test_generic_proxy ;;
    esac

    echo ""
    echo "=========================================="
    echo "SUMMARY: $IMAGE (type=$proxy_type)"
    echo "=========================================="
    echo -e "  ${GREEN}PASS${NC}: $PASS_COUNT"
    echo -e "  ${RED}FAIL${NC}: $FAIL_COUNT"
    echo -e "  ${YELLOW}SKIP${NC}: $SKIP_COUNT"
    echo "  TOTAL: $TOTAL"
    echo "=========================================="

    [ $FAIL_COUNT -eq 0 ]
}

main "$@"
