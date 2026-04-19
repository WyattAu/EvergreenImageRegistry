#!/bin/bash
# =============================================================================
# ADVERSARIAL TEST SUITE
# =============================================================================
# Tests that containers CANNOT be compromised through common attack vectors.
# Each test verifies that a specific adversarial action MUST FAIL.
#
# Usage: IMAGE=<image> ./test_adversarial.sh
#        ./test_adversarial.sh <image>
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
    if [ -n "$CONTAINER_NAME" ] && docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    fi
    if [ -n "$CONTAINER_NAME" ] && docker ps -aq -f name="$CONTAINER_NAME" | grep -q .; then
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

start_container() {
    CONTAINER_NAME="advtest-$(date +%s)-$$"
    local run_args=()
    if [ "${ADVERSARIAL_EXTRA_ARGS:-}" != "" ]; then
        read -ra run_args <<< "$ADVERSARIAL_EXTRA_ARGS"
    fi
    if ! docker run -d --name "$CONTAINER_NAME" "${run_args[@]}" "$IMAGE" >/dev/null 2>&1; then
        return 1
    fi
    local max_wait="${STARTUP_TIMEOUT:-10}"
    local waited=0
    while [ $waited -lt $max_wait ]; do
        if ! docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
            return 1
        fi
        sleep 1
        waited=$((waited + 1))
    done
    return 0
}

assert_exec_fails() {
    local test_id="$1" desc="$2"
    shift 2
    if [ -z "$CONTAINER_NAME" ]; then
        record "$test_id" "SKIP" "$desc (container not running)"
        return
    fi
    if docker exec "$CONTAINER_NAME" "$@" >/dev/null 2>&1; then
        record "$test_id" "FAIL" "$desc (command succeeded, should have failed)"
    else
        record "$test_id" "PASS" "$desc"
    fi
}

assert_file_not_writable() {
    local test_id="$1" desc="$2" filepath="$3"
    if [ -z "$CONTAINER_NAME" ]; then
        record "$test_id" "SKIP" "$desc (container not running)"
        return
    fi
    if docker exec "$CONTAINER_NAME" sh -c "test -w '$filepath'" >/dev/null 2>&1; then
        record "$test_id" "FAIL" "$desc ($filepath is writable)"
    else
        record "$test_id" "PASS" "$desc"
    fi
}

assert_binary_not_writable() {
    local test_id="$1" desc="$2" binary="$3"
    if [ -z "$CONTAINER_NAME" ]; then
        record "$test_id" "SKIP" "$desc (container not running)"
        return
    fi
    local perms
    perms=$(docker exec "$CONTAINER_NAME" stat -c '%a' "$binary" 2>/dev/null || echo "000")
    if echo "$perms" | grep -qE '^[2-7]'; then
        record "$test_id" "FAIL" "$desc ($binary is writable, perms=$perms)"
    else
        record "$test_id" "PASS" "$desc"
    fi
}

# =============================================================================
# SHELL ESCAPE TESTS
# =============================================================================

test_shell_escapes() {
    echo ""
    echo "--- Shell Escape Tests ---"
    assert_exec_fails "SH-001" "docker exec /bin/sh" /bin/sh -c "exit 0"
    assert_exec_fails "SH-002" "docker exec /bin/bash" /bin/bash -c "exit 0"
    assert_exec_fails "SH-003" "docker exec sh -c id" sh -c "id"
    assert_exec_fails "SH-004" "docker exec ash" ash -c "exit 0"
    assert_exec_fails "SH-005" "docker exec dash" dash -c "exit 0"
}

# =============================================================================
# PRIVILEGE ESCALATION TESTS
# =============================================================================

test_privilege_escalation() {
    echo ""
    echo "--- Privilege Escalation Tests ---"
    assert_exec_fails "PE-001" "docker exec su" su -c "exit 0"
    assert_exec_fails "PE-002" "docker exec sudo" sudo true
    assert_exec_fails "PE-003" "docker exec chmod 4755 /tmp" chmod 4755 /tmp
    assert_exec_fails "PE-004" "docker exec chown root /tmp" chown root /tmp
}

# =============================================================================
# PACKAGE MANAGER TESTS
# =============================================================================

test_package_managers() {
    echo ""
    echo "--- Package Manager Tests ---"
    assert_exec_fails "PM-001" "docker exec apt-get update" apt-get update
    assert_exec_fails "PM-002" "docker exec apt install curl" apt install -y curl
    assert_exec_fails "PM-003" "docker exec apk add curl" apk add curl
    assert_exec_fails "PM-004" "docker exec dnf install curl" dnf install -y curl
}

# =============================================================================
# NETWORK EXFILTRATION TESTS
# =============================================================================

test_network_exfiltration() {
    echo ""
    echo "--- Network Exfiltration Tests ---"
    local net_container="advtest-net-$(date +%s)-$$"
    if docker run -d --network=none --name "$net_container" "$IMAGE" >/dev/null 2>&1; then
        local waited=0
        local running=false
        while [ $waited -lt "${STARTUP_TIMEOUT:-10}" ]; do
            if docker ps -q -f name="$net_container" | grep -q .; then
                running=true
                break
            fi
            sleep 1
            waited=$((waited + 1))
        done
        if [ "$running" = "true" ]; then
            record "NE-001" "PASS" "Container starts with --network=none"
        else
            record "NE-001" "FAIL" "Container fails to start with --network=none"
        fi
        docker rm -f "$net_container" >/dev/null 2>&1 || true
    else
        record "NE-001" "SKIP" "Container cannot start with --network=none"
    fi

    if [ -n "$CONTAINER_NAME" ] && docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        local exposed_ports
        exposed_ports=$(docker inspect "$IMAGE" --format='{{json .Config.ExposedPorts}}' 2>/dev/null || echo "{}")
        local expected_ports="${EXPOSED_PORTS:-}"
        if [ -n "$expected_ports" ]; then
            local listening_ports
            listening_ports=$(docker exec "$CONTAINER_NAME" ss -tlnp 2>/dev/null | grep -oP ':\K\d+' || echo "")
            local unexpected=""
            for port in $listening_ports; do
                if ! echo "$expected_ports $port" | grep -qw "$port"; then
                    unexpected="$unexpected $port"
                fi
            done
            if [ -z "$unexpected" ]; then
                record "NE-002" "PASS" "No unexpected listening ports"
            else
                record "NE-002" "FAIL" "Unexpected listening ports:$unexpected"
            fi
        else
            record "NE-002" "SKIP" "No EXPOSED_PORTS defined, skipping port check"
        fi
    else
        record "NE-002" "SKIP" "Container not running, skipping port check"
    fi
}

# =============================================================================
# FILESYSTEM INTEGRITY TESTS
# =============================================================================

test_filesystem_integrity() {
    echo ""
    echo "--- Filesystem Integrity Tests ---"

    local ro_container="advtest-ro-$(date +%s)-$$"
    if docker run --rm --read-only "$IMAGE" true >/dev/null 2>&1; then
        record "FI-001" "PASS" "Root filesystem accepts --read-only flag"
    else
        record "FI-001" "SKIP" "Container cannot run with --read-only (may need tmpfs mounts)"
    fi

    assert_file_not_writable "FI-002" "/etc/passwd is not writable" /etc/passwd

    local entrypoint_binary
    entrypoint_binary=$(docker inspect "$IMAGE" --format='{{(index .Config.Entrypoint 0)}}' 2>/dev/null || echo "")
    if [ -n "$entrypoint_binary" ] && [ "$entrypoint_binary" != "null" ] && [ "$entrypoint_binary" != "<no value>" ]; then
        assert_binary_not_writable "FI-003" "ENTRYPOINT binary is not writable" "$entrypoint_binary"
    else
        record "FI-003" "SKIP" "No ENTRYPOINT binary detected"
    fi
}

# =============================================================================
# DEBUG TOOL TESTS
# =============================================================================

test_debug_tools() {
    echo ""
    echo "--- Debug Tool Tests ---"
    assert_exec_fails "DT-001" "docker exec gdb" gdb --version
    assert_exec_fails "DT-002" "docker exec strace" strace -V
    assert_exec_fails "DT-003" "docker exec ltrace" ltrace -V
    assert_exec_fails "DT-004" "docker exec tcpdump" tcpdump --version
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    if [ -z "$IMAGE" ]; then
        echo "Usage: IMAGE=<image> $0"
        echo "       $0 <image>"
        echo ""
        echo "Environment variables:"
        echo "  IMAGE              Container image to test (required)"
        echo "  STARTUP_TIMEOUT    Seconds to wait for container startup (default: 10)"
        echo "  EXPOSED_PORTS      Space-separated list of expected listening ports"
        echo "  ADVERSARIAL_EXTRA_ARGS  Additional docker run arguments"
        exit 1
    fi

    echo "=========================================="
    echo "ADVERSARIAL TEST SUITE"
    echo "Image: $IMAGE"
    echo "=========================================="

    if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
        echo "ERROR: Image '$IMAGE' not found locally"
        exit 1
    fi

    if start_container; then
        echo "Container started: $CONTAINER_NAME"
    else
        echo "WARNING: Container failed to start - running non-container tests only"
        CONTAINER_NAME=""
    fi

    test_shell_escapes
    test_privilege_escalation
    test_package_managers
    test_network_exfiltration
    test_filesystem_integrity
    test_debug_tools

    echo ""
    echo "=========================================="
    echo "SUMMARY: $IMAGE"
    echo "=========================================="
    echo -e "  ${GREEN}PASS${NC}: $PASS_COUNT"
    echo -e "  ${RED}FAIL${NC}: $FAIL_COUNT"
    echo -e "  ${YELLOW}SKIP${NC}: $SKIP_COUNT"
    echo "  TOTAL: $TOTAL"
    echo "=========================================="

    if [ $FAIL_COUNT -gt 0 ]; then
        exit 1
    fi
    exit 0
}

main "$@"
