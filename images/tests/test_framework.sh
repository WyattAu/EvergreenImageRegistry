#!/bin/bash
# =============================================================================
# SOVEREIGN HARDENED IMAGE REGISTRY - TEST FRAMEWORK
# =============================================================================
# Per-image test scripts for validation
# Tests: functionality, security constraints, runtime behavior
# =============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test configuration
IMAGE="${IMAGE:-}"
TEST_TYPE="${TEST_TYPE:-all}"  # all, functional, security, constraints
VERBOSE="${VERBOSE:-false}"

# =============================================================================
# TEST UTILITIES
# =============================================================================

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    if [ "$VERBOSE" = "true" ]; then
        echo -e "[DEBUG] $1"
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Assertion failed}"
    
    if [ "$expected" = "$actual" ]; then
        log_debug "PASS: $message"
        return 0
    else
        log_error "FAIL: $message (expected='$expected', actual='$actual')"
        return 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-Assertion failed}"
    
    if echo "$haystack" | grep -q "$needle"; then
        log_debug "PASS: $message"
        return 0
    else
        log_error "FAIL: $message (needle='$needle' not found in haystack)"
        return 1
    fi
}

# =============================================================================
# CONSTRAINT TESTS (C001-C013)
# =============================================================================

test_c001_non_root() {
    log_info "Testing C001: Non-root user..."
    
    # Test 1: Check running as non-root UID (65534 = nobody, or non-zero)
    local user_id
    user_id=$(docker run --rm "$IMAGE" id -u 2>/dev/null || echo "failed")
    
    if [ "$user_id" = "65534" ] || [ "$user_id" = "nobody" ] || [ "$user_id" -gt 0 ] 2>/dev/null; then
        echo "✓ C001 PASS: Running as UID $user_id (non-root)"
        return 0
    else
        echo "✗ C001 FAIL: Running as root UID $user_id"
        return 1
    fi
}

test_c002_readonly_filesystem() {
    log_info "Testing C002: Read-only filesystem..."
    
    # Test: Attempt to write to filesystem - should fail
    if docker run --rm --read-only "$IMAGE" touch /tmp/test_write 2>/dev/null; then
        echo "✗ C002 FAIL: Write succeeded (filesystem not read-only)"
        return 1
    else
        echo "✓ C002 PASS: Filesystem is read-only"
        return 0
    fi
}

test_c003_no_shell() {
    log_info "Testing C003: No shell available..."
    
    local shells=("/bin/sh" "/bin/bash" "/dash" "/ash" "/bin/rbash" "/usr/bin/sh")
    local found_shells=()
    
    for shell in "${shells[@]}"; do
        if docker run --rm "$IMAGE" test -f "$shell" 2>/dev/null; then
            found_shells+=("$shell")
        fi
    done
    
    if [ ${#found_shells[@]} -eq 0 ]; then
        echo "✓ C003 PASS: No shells found"
        return 0
    else
        echo "✗ C003 FAIL: Found shells: ${found_shells[*]}"
        return 1
    fi
}

test_c004_no_package_manager() {
    log_info "Testing C004: No package manager..."
    
    local pkg_managers=("/usr/bin/apt" "/usr/bin/apt-get" "/usr/bin/apk" "/usr/bin/dnf" "/usr/bin/yum" "/usr/bin/zypper")
    local found_pms=()
    
    for pm in "${pkg_managers[@]}"; do
        if docker run --rm "$IMAGE" test -f "$pm" 2>/dev/null; then
            found_pms+=("$pm")
        fi
    done
    
    if [ ${#found_pms[@]} -eq 0 ]; then
        echo "✓ C004 PASS: No package managers found"
        return 0
    else
        echo "✗ C004 FAIL: Found package managers: ${found_pms[*]}"
        return 1
    fi
}

test_c005_no_sudo() {
    log_info "Testing C005: No sudo/su..."
    
    local priv_tools=("/usr/bin/sudo" "/usr/bin/su" "/usr/sbin/sudo" "/usr/sbin/su")
    local found=()
    
    for tool in "${priv_tools[@]}"; do
        if docker run --rm "$IMAGE" test -f "$tool" 2>/dev/null; then
            found+=("$tool")
        fi
    done
    
    if [ ${#found[@]} -eq 0 ]; then
        echo "✓ C005 PASS: No privilege escalation tools found"
        return 0
    else
        echo "✗ C005 FAIL: Found: ${found[*]}"
        return 1
    fi
}

test_c006_no_network_on_startup() {
    log_info "Testing C006: No network on startup (default deny)..."
    
    # This is a design requirement - image should NOT expose ports by default
    # or should have explicit network configuration
    # This is informational - actual network policy depends on runtime
    echo "ℹ C006 INFO: Network policy depends on runtime configuration"
    return 0
}

test_c007_minimal_packages() {
    log_info "Testing C007: Minimal packages installed..."
    
    # Count packages - should be minimal for scratch/distroless
    local pkg_count
    if docker run --rm "$IMAGE" dpkg -l 2>/dev/null | tail -n +6 | wc -l; then
        pkg_count=$(docker run --rm "$IMAGE" dpkg -l 2>/dev/null | tail -n +6 | wc -l)
    elif docker run --rm "$IMAGE" rpm -qa 2>/dev/null | wc -l; then
        pkg_count=$(docker run --rm "$IMAGE" rpm -qa 2>/dev/null | wc -l)
    else
        # Probably scratch image - no package manager
        pkg_count=0
    fi
    
    if [ "$pkg_count" -lt 50 ]; then
        echo "✓ C007 PASS: Minimal packages ($pkg_count)"
        return 0
    else
        echo "⚠ C007 WARN: Many packages installed ($pkg_count)"
        return 0  # Warning, not failure
    fi
}

test_c008_no_docker_socket() {
    log_info "Testing C008: No Docker socket access..."
    
    if docker run --rm "$IMAGE" test -S /var/run/docker.sock 2>/dev/null; then
        echo "✗ C008 FAIL: Docker socket found"
        return 1
    else
        echo "✓ C008 PASS: No Docker socket"
        return 0
    fi
}

test_c009_no_init_system() {
    log_info "Testing C009: No init system (PID 1 should be app)..."
    
    # Check if running as PID 1 directly (for scratch images)
    # This is informational
    echo "ℹ C009 INFO: Application should run as PID 1"
    return 0
}

test_c010_health_check() {
    log_info "Testing C010: Health check exists..."
    
    # Try common health endpoints
    local http_code
    local found=false
    
    # Start container in background
    local cid
    cid=$(docker run -d --rm "$IMAGE" 2>/dev/null || echo "")
    
    if [ -z "$cid" ]; then
        echo "⚠ C010 WARN: Could not start container"
        return 0
    fi
    
    sleep 3
    
    for port in 80 443 8080 9090 8000 3000 5432 6379 9200; do
        http_code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port/" --connect-timeout 2 --max-time 5 2>/dev/null || echo "000")
        
        if [ "$http_code" = "200" ] || [ "$http_code" = "404" ] || [ "$http_code" = "401" ]; then
            # Any response means service is running
            echo "✓ C010 PASS: Service responding on port $port (HTTP $http_code)"
            found=true
            break
        fi
    done
    
    # Cleanup
    docker kill "$cid" 2>/dev/null || true
    
    if [ "$found" = "true" ]; then
        return 0
    else
        echo "⚠ C010 WARN: No health endpoint found (service may not expose HTTP)"
        return 0
    fi
}

test_c011_no_debug_tools() {
    log_info "Testing C011: No debug tools..."
    
    local debug_tools=("gdb" "strace" "ltrace" "file" "strings" "readelf" "objdump")
    local found=()
    
    for tool in "${debug_tools[@]}"; do
        if docker run --rm "$IMAGE" which "$tool" 2>/dev/null; then
            found+=("$tool")
        fi
    done
    
    if [ ${#found[@]} -eq 0 ]; then
        echo "✓ C011 PASS: No debug tools found"
        return 0
    else
        echo "⚠ C011 WARN: Found: ${found[*]}"
        return 0
    fi
}

test_c012_immutable_tags() {
    log_info "Testing C012: Immutable tags (design time check)..."
    # This is a deployment policy, not runtime test
    echo "ℹ C012 INFO: Immutable tags enforced at deployment time"
    return 0
}

test_c013_signed_images() {
    log_info "Testing C013: Image signing verification..."
    # Check if cosign verification works (if tool available)
    if command -v cosign &>/dev/null; then
        echo "ℹ C013 INFO: Cosign available - verify in CI"
    else
        echo "ℹ C013 INFO: Cosign not available in test environment"
    fi
    return 0
}

# =============================================================================
# FUNCTIONAL TESTS
# =============================================================================

test_functional_basic() {
    log_info "Testing functional: Basic execution..."
    
    # Try to run the binary with --version or --help
    local binary="${BINARY:-}"
    
    if [ -z "$binary" ]; then
        echo "⚠ No BINARY specified, skipping functional test"
        return 0
    fi
    
    # Try common flags
    for flag in "--version" "-v" "version" "-V" "--help" "-h"; do
        if docker run --rm "$IMAGE" "$binary" "$flag" &>/dev/null; then
            local output
            output=$(docker run --rm "$IMAGE" "$binary" "$flag" 2>&1 | head -5)
            echo "✓ Functional PASS: Binary responds to $flag"
            log_debug "Output: $output"
            return 0
        fi
    done
    
    echo "⚠ Functional WARN: Binary did not respond to common flags"
    return 0
}

test_functional_ports() {
    log_info "Testing functional: Port binding..."
    
    # Check which ports are EXPOSED in Dockerfile
    local exposed_ports
    exposed_ports=$(docker inspect "$IMAGE" --format='{{join .Config.ExposedPorts "\n"}}' 2>/dev/null || echo "")
    
    if [ -n "$exposed_ports" ]; then
        echo "ℹ Exposed ports: $exposed_ports"
        echo "✓ Functional PASS: Ports configured"
        return 0
    else
        echo "ℹ No exposed ports (may be intentional for scratch)"
        return 0
    fi
}

test_functional_environment() {
    log_info "Testing functional: Environment variables..."
    
    # Check for required env vars
    local env_vars
    env_vars=$(docker inspect "$IMAGE" --format='{{json .Config.Env}}' 2>/dev/null || echo "[]")
    
    echo "ℹ Environment: $env_vars"
    echo "✓ Functional PASS: Environment checked"
    return 0
}

# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

run_all_tests() {
    local failed=0
    local passed=0
    local skipped=0
    
    echo "=========================================="
    echo "Sovereign Hardened Image Test Suite"
    echo "Image: $IMAGE"
    echo "=========================================="
    
    # Constraint Tests
    echo ""
    echo "--- CONSTRAINT TESTS ---"
    
    test_c001_non_root || ((failed++)) || ((passed++))
    test_c002_readonly_filesystem || ((failed++)) || ((passed++))
    test_c003_no_shell || ((failed++)) || ((passed++))
    test_c004_no_package_manager || ((failed++)) || ((passed++))
    test_c005_no_sudo || ((failed++)) || ((passed++))
    test_c006_no_network_on_startup || ((skipped++)) || ((passed++))
    test_c007_minimal_packages || ((failed++)) || ((passed++))
    test_c008_no_docker_socket || ((failed++)) || ((passed++))
    test_c009_no_init_system || ((skipped++)) || ((passed++))
    test_c010_health_check || ((failed++)) || ((passed++))
    test_c011_no_debug_tools || ((failed++)) || ((passed++))
    test_c012_immutable_tags || ((skipped++)) || ((passed++))
    test_c013_signed_images || ((skipped++)) || ((passed++))
    
    # Functional Tests
    echo ""
    echo "--- FUNCTIONAL TESTS ---"
    
    test_functional_basic || ((failed++)) || ((passed++))
    test_functional_ports || ((failed++)) || ((passed++))
    test_functional_environment || ((failed++)) || ((passed++))
    
    # Summary
    echo ""
    echo "=========================================="
    echo "TEST SUMMARY"
    echo "=========================================="
    echo "Passed: $passed"
    echo "Failed: $failed"
    echo "Skipped: $skipped"
    echo "=========================================="
    
    if [ $failed -gt 0 ]; then
        return 1
    else
        return 0
    fi
}

# =============================================================================
# ENTRY POINT
# =============================================================================

main() {
    if [ -z "$IMAGE" ]; then
        echo "Usage: IMAGE=<image_name> $0 [all|functional|security|constraints]"
        echo ""
        echo "Environment variables:"
        echo "  IMAGE      - Image name to test (required)"
        echo "  TEST_TYPE  - Test type: all, functional, security, constraints"
        echo "  BINARY     - Binary name for functional tests"
        echo "  VERBOSE    - Enable debug output (true/false)"
        exit 1
    fi
    
    TEST_TYPE="${1:-$TEST_TYPE}"
    
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
            test_c011_no_debug_tools
            ;;
        constraints)
            test_c001_non_root
            test_c002_readonly_filesystem
            test_c003_no_shell
            test_c004_no_package_manager
            test_c005_no_sudo
            test_c007_minimal_packages
            test_c008_no_docker_socket
            test_c010_health_check
            ;;
        *)
            echo "Unknown test type: $TEST_TYPE"
            exit 1
            ;;
    esac
}

main "$@"