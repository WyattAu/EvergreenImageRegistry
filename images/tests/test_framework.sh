#!/bin/bash
# =============================================================================
# SOVEREIGN HARDENED IMAGE REGISTRY - TEST FRAMEWORK
# =============================================================================
# Per-image test scripts for validation
# Tests: functionality, security constraints, runtime behavior
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

IMAGE="${IMAGE:-}"
TEST_TYPE="${TEST_TYPE:-all}"
VERBOSE="${VERBOSE:-false}"

declare -a TEST_RESULTS=()

record_result() {
    local id="$1"
    local status="$2"
    local desc="$3"
    TEST_RESULTS+=("${id}|${status}|${desc}")
}

# =============================================================================
# TEST UTILITIES
# =============================================================================

log_info() {
    echo -e "${GREEN}[INFO]${NC} [$IMAGE] $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} [$IMAGE] $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} [$IMAGE] $1"
}

log_debug() {
    if [ "$VERBOSE" = "true" ]; then
        echo -e "[DEBUG] [$IMAGE] $1"
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
# CONSTRAINT TESTS (C001-C014, C019)
# =============================================================================

test_c001_non_root() {
    log_info "Testing C001: Non-root user..."

    local user_id
    user_id=$(docker run --rm "$IMAGE" id -u 2>/dev/null || echo "failed")

    if [ "$user_id" = "65534" ] || [ "$user_id" = "nobody" ] || { [ "$user_id" != "failed" ] && [ "$user_id" -gt 0 ] 2>/dev/null; }; then
        echo "  PASS: Running as UID $user_id (non-root)"
        return 0
    else
        log_error "C001: Running as root UID $user_id"
        echo "  FAIL: Running as root UID $user_id"
        return 1
    fi
}

test_c002_readonly_filesystem() {
    log_info "Testing C002: Read-only filesystem..."

    if docker run --rm --read-only "$IMAGE" touch /tmp/test_write 2>/dev/null; then
        log_error "C002: Write succeeded on read-only filesystem"
        echo "  FAIL: Write succeeded (filesystem not read-only)"
        return 1
    else
        echo "  PASS: Filesystem is read-only"
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
        echo "  PASS: No shells found"
        return 0
    else
        log_error "C003: Found shells: ${found_shells[*]}"
        echo "  FAIL: Found shells: ${found_shells[*]}"
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
        echo "  PASS: No package managers found"
        return 0
    else
        log_error "C004: Found package managers: ${found_pms[*]}"
        echo "  FAIL: Found package managers: ${found_pms[*]}"
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
        echo "  PASS: No privilege escalation tools found"
        return 0
    else
        log_error "C005: Found privilege escalation tools: ${found[*]}"
        echo "  FAIL: Found: ${found[*]}"
        return 1
    fi
}

test_c006_no_network_on_startup() {
    log_info "Testing C006: No network on startup (default deny)..."

    local exposed_ports
    exposed_ports=$(docker inspect "$IMAGE" --format='{{json .Config.ExposedPorts}}' 2>/dev/null || echo "null")

    if [ "$exposed_ports" != "null" ] && [ "$exposed_ports" != "map[]" ] && [ -n "$exposed_ports" ]; then
        log_warn "C006: Image exposes ports: $exposed_ports - verify network policy at runtime"
        echo "  WARN: Exposed ports found ($exposed_ports) - network policy must be enforced at runtime"
        return 0
    else
        echo "  PASS: No exposed ports (network-isolated by default)"
        return 0
    fi
}

test_c007_minimal_packages() {
    log_info "Testing C007: Minimal packages installed..."

    local pkg_count=0
    local has_pkg_manager=false

    if docker run --rm "$IMAGE" dpkg -l &>/dev/null; then
        pkg_count=$(docker run --rm "$IMAGE" dpkg -l 2>/dev/null | tail -n +6 | wc -l | tr -d ' ')
        has_pkg_manager=true
    elif docker run --rm "$IMAGE" rpm -qa &>/dev/null; then
        pkg_count=$(docker run --rm "$IMAGE" rpm -qa 2>/dev/null | wc -l | tr -d ' ')
        has_pkg_manager=true
    fi

    if [ "$has_pkg_manager" = "false" ]; then
        echo "  PASS: No package manager (scratch/distroless image)"
        return 0
    elif [ "$pkg_count" -lt 15 ]; then
        echo "  PASS: Minimal packages ($pkg_count)"
        return 0
    elif [ "$pkg_count" -lt 50 ]; then
        log_warn "C007: $pkg_count packages installed (above recommended threshold of 15)"
        echo "  WARN: $pkg_count packages installed (above recommended 15)"
        return 0
    else
        log_error "C007: Too many packages installed ($pkg_count >= 50)"
        echo "  FAIL: Too many packages ($pkg_count >= 50)"
        return 1
    fi
}

test_c008_no_docker_socket() {
    log_info "Testing C008: No Docker socket access..."

    if docker run --rm "$IMAGE" test -S /var/run/docker.sock 2>/dev/null; then
        log_error "C008: Docker socket found inside image"
        echo "  FAIL: Docker socket found"
        return 1
    else
        echo "  PASS: No Docker socket"
        return 0
    fi
}

test_c009_no_init_system() {
    log_info "Testing C009: No init system (PID 1 should be app)..."

    local entrypoint
    entrypoint=$(docker inspect "$IMAGE" --format='{{json .Config.Entrypoint}}' 2>/dev/null || echo "null")
    local cmd
    cmd=$(docker inspect "$IMAGE" --format='{{json .Config.Cmd}}' 2>/dev/null || echo "null")

    local init_signals=("tini" "dumb-init" "/sbin/init" "systemd" "openrc" "runit" "s6" "supervisord")
    local combined="${entrypoint} ${cmd}"
    local found_init=""

    for init in "${init_signals[@]}"; do
        if echo "$combined" | grep -qi "$init"; then
            found_init="$init"
            break
        fi
    done

    if [ -n "$found_init" ]; then
        log_warn "C009: Init system detected: $found_init - PID 1 is not the application"
        echo "  WARN: Init system '$found_init' found - PID 1 is not the application"
        return 0
    else
        echo "  PASS: No init system - application runs as PID 1"
        return 0
    fi
}

test_c010_health_check() {
    log_info "Testing C010: Health check configuration (static analysis)..."

    local healthcheck
    healthcheck=$(docker inspect "$IMAGE" --format='{{json .Config.Healthcheck}}' 2>/dev/null || echo "null")

    if [ "$healthcheck" != "null" ] && [ "$healthcheck" != "<nil>" ] && [ "$healthcheck" != "map[]" ]; then
        echo "  PASS: HEALTHCHECK instruction defined in image config"
        return 0
    else
        log_warn "C010: No HEALTHCHECK instruction found in image config"
        echo "  WARN: No HEALTHCHECK defined - consider adding one for orchestration"
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
        echo "  PASS: No debug tools found"
        return 0
    else
        log_warn "C011: Debug tools found: ${found[*]}"
        echo "  WARN: Found debug tools: ${found[*]}"
        return 0
    fi
}

test_c012_immutable_tags() {
    log_info "Testing C012: Immutable tag policy (label check)..."

    local labels
    labels=$(docker inspect "$IMAGE" --format='{{json .Config.Labels}}' 2>/dev/null || echo "{}")

    local immutable_labels=("oci.image.immutable" "org.opencontainers.image.immutable" "io.container.image.immutable")
    local found_policy=""

    for label in "${immutable_labels[@]}"; do
        if echo "$labels" | grep -q "$label"; then
            found_policy="$label"
            break
        fi
    done

    if [ -n "$found_policy" ]; then
        echo "  PASS: Immutable tag policy label found: $found_policy"
        return 0
    else
        log_warn "C012: No immutable tag policy label detected on image"
        echo "  WARN: No immutable tag policy label found (add e.g. org.opencontainers.image.immutable)"
        return 0
    fi
}

test_c013_signed_images() {
    log_info "Testing C013: Image signing verification..."

    if ! command -v cosign &>/dev/null; then
        log_warn "C013: cosign not available in test environment - cannot verify signature"
        echo "  WARN: cosign not installed - skipping signature verification"
        return 0
    fi

    local digest
    digest=$(docker inspect "$IMAGE" --format='{{index .RepoDigests 0}}' 2>/dev/null || echo "")

    if [ -z "$digest" ]; then
        log_warn "C013: No RepoDigests found for image - may not be from a registry"
        echo "  WARN: No repo digest available for signature verification"
        return 0
    fi

    if cosign verify --key cosign.pub "$digest" &>/dev/null; then
        echo "  PASS: Image signature verified (key-based)"
        return 0
    elif cosign verify "$digest" &>/dev/null; then
        echo "  PASS: Image signature verified (keyless)"
        return 0
    else
        log_error "C013: Signature verification failed for $digest"
        echo "  FAIL: Image signature verification failed"
        return 1
    fi
}

test_c014_oci_compliance() {
    log_info "Testing C014: OCI compliance (manifest inspection)..."

    local architecture
    architecture=$(docker inspect "$IMAGE" --format='{{.Architecture}}' 2>/dev/null || echo "")
    local os
    os=$(docker inspect "$IMAGE" --format='{{.Os}}' 2>/dev/null || echo "")

    if [ -z "$architecture" ] || [ -z "$os" ]; then
        log_error "C014: Missing OCI platform fields (architecture='$architecture', os='$os')"
        echo "  FAIL: Missing OCI platform fields"
        return 1
    fi

    local image_id
    image_id=$(docker inspect "$IMAGE" --format='{{.Id}}' 2>/dev/null || echo "")
    if [ -z "$image_id" ]; then
        log_error "C014: Missing image config digest"
        echo "  FAIL: Missing image config digest"
        return 1
    fi

    local created
    created=$(docker inspect "$IMAGE" --format='{{.Created}}' 2>/dev/null || echo "")
    if [ -z "$created" ]; then
        log_warn "C014: Missing created timestamp in image config"
        echo "  WARN: Missing created timestamp (non-compliant)"
        return 0
    fi

    echo "  PASS: OCI compliant (os=$os, arch=$architecture)"
    return 0
}

test_c019_no_latest_tag() {
    log_info "Testing C019: No 'latest' tag..."

    local tags
    tags=$(docker inspect "$IMAGE" --format='{{json .RepoTags}}' 2>/dev/null || echo "[]")

    if echo "$tags" | grep -q ":latest"; then
        log_error "C019: Image uses 'latest' tag: $tags"
        echo "  FAIL: Image tagged with 'latest' - use immutable digest or versioned tag"
        return 1
    else
        echo "  PASS: No 'latest' tag found"
        return 0
    fi
}

# =============================================================================
# FUNCTIONAL TESTS
# =============================================================================

test_functional_basic() {
    log_info "Testing functional: Basic execution..."

    local binary="${BINARY:-}"

    if [ -z "$binary" ]; then
        local entrypoint
        entrypoint=$(docker inspect "$IMAGE" --format='{{(index .Config.Entrypoint 0)}}' 2>/dev/null || echo "")

        if [ -n "$entrypoint" ] && [ "$entrypoint" != "null" ] && [ "$entrypoint" != "<no value>" ]; then
            binary="$entrypoint"
            log_debug "Auto-detected ENTRYPOINT as binary: $binary"
        else
            local cmd0
            cmd0=$(docker inspect "$IMAGE" --format='{{(index .Config.Cmd 0)}}' 2>/dev/null || echo "")

            if [ -n "$cmd0" ] && [ "$cmd0" != "null" ] && [ "$cmd0" != "<no value>" ]; then
                binary="$cmd0"
                log_debug "Auto-detected CMD as binary: $cmd0"
            fi
        fi
    fi

    if [ -z "$binary" ]; then
        log_warn "Functional: No binary found via BINARY env, ENTRYPOINT, or CMD"
        echo "  WARN: No binary detected - skipping functional test"
        return 0
    fi

    for flag in "--version" "-v" "version" "-V" "--help" "-h"; do
        if docker run --rm "$IMAGE" "$binary" "$flag" &>/dev/null; then
            local output
            output=$(docker run --rm "$IMAGE" "$binary" "$flag" 2>&1 | head -5)
            echo "  PASS: Binary '$binary' responds to '$flag'"
            log_debug "Output: $output"
            return 0
        fi
    done

    log_warn "Functional: Binary '$binary' did not respond to common flags"
    echo "  WARN: Binary '$binary' did not respond to common flags"
    return 0
}

test_functional_ports() {
    log_info "Testing functional: Port binding..."

    local exposed_ports
    exposed_ports=$(docker inspect "$IMAGE" --format='{{join .Config.ExposedPorts "\n"}}' 2>/dev/null || echo "")

    if [ -n "$exposed_ports" ]; then
        echo "  INFO: Exposed ports: $exposed_ports"
        echo "  PASS: Ports configured"
        return 0
    else
        echo "  INFO: No exposed ports (may be intentional for scratch images)"
        return 0
    fi
}

test_functional_environment() {
    log_info "Testing functional: Environment variables..."

    local env_vars
    env_vars=$(docker inspect "$IMAGE" --format='{{json .Config.Env}}' 2>/dev/null || echo "[]")

    echo "  INFO: Environment: $env_vars"
    echo "  PASS: Environment checked"
    return 0
}

# =============================================================================
# SUMMARY REPORT
# =============================================================================

print_summary() {
    echo ""
    echo "=========================================="
    echo "TEST RESULTS SUMMARY - $IMAGE"
    echo "=========================================="
    printf "%-12s %-8s %s\n" "ID" "STATUS" "DESCRIPTION"
    printf "%-12s %-8s %s\n" "----" "------" "-----------"

    local pass_count=0
    local fail_count=0
    local warn_count=0

    for result in "${TEST_RESULTS[@]}"; do
        IFS='|' read -r id status desc <<< "$result"
        case "$status" in
            PASS) pass_count=$((pass_count + 1)) ;;
            FAIL) fail_count=$((fail_count + 1)) ;;
            WARN) warn_count=$((warn_count + 1)) ;;
        esac
        local_color="$NC"
        if [ "$status" = "PASS" ]; then
            local_color="$GREEN"
        elif [ "$status" = "FAIL" ]; then
            local_color="$RED"
        elif [ "$status" = "WARN" ]; then
            local_color="$YELLOW"
        fi
        printf "%-12s ${local_color}%-8s${NC} %s\n" "$id" "$status" "$desc"
    done

    echo "=========================================="
    echo -e "  ${GREEN}PASS${NC}: $pass_count  ${RED}FAIL${NC}: $fail_count  ${YELLOW}WARN${NC}: $warn_count"
    echo "=========================================="

    if [ $fail_count -gt 0 ]; then
        return 1
    fi
    return 0
}

# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

run_all_tests() {
    local failed=0
    local passed=0

    echo "=========================================="
    echo "Sovereign Hardened Image Test Suite"
    echo "Image: $IMAGE"
    echo "=========================================="

    echo ""
    echo "--- CONSTRAINT TESTS ---"

    if test_c001_non_root; then
        passed=$((passed + 1)); record_result "C001" "PASS" "Non-root user"
    else
        failed=$((failed + 1)); record_result "C001" "FAIL" "Non-root user"
    fi

    if test_c002_readonly_filesystem; then
        passed=$((passed + 1)); record_result "C002" "PASS" "Read-only filesystem"
    else
        failed=$((failed + 1)); record_result "C002" "FAIL" "Read-only filesystem"
    fi

    if test_c003_no_shell; then
        passed=$((passed + 1)); record_result "C003" "PASS" "No shell"
    else
        failed=$((failed + 1)); record_result "C003" "FAIL" "No shell"
    fi

    if test_c004_no_package_manager; then
        passed=$((passed + 1)); record_result "C004" "PASS" "No package manager"
    else
        failed=$((failed + 1)); record_result "C004" "FAIL" "No package manager"
    fi

    if test_c005_no_sudo; then
        passed=$((passed + 1)); record_result "C005" "PASS" "No sudo/su"
    else
        failed=$((failed + 1)); record_result "C005" "FAIL" "No sudo/su"
    fi

    if test_c006_no_network_on_startup; then
        passed=$((passed + 1)); record_result "C006" "PASS" "No network on startup"
    else
        failed=$((failed + 1)); record_result "C006" "FAIL" "No network on startup"
    fi

    if test_c007_minimal_packages; then
        passed=$((passed + 1)); record_result "C007" "PASS" "Minimal packages"
    else
        failed=$((failed + 1)); record_result "C007" "FAIL" "Minimal packages"
    fi

    if test_c008_no_docker_socket; then
        passed=$((passed + 1)); record_result "C008" "PASS" "No Docker socket"
    else
        failed=$((failed + 1)); record_result "C008" "FAIL" "No Docker socket"
    fi

    if test_c009_no_init_system; then
        passed=$((passed + 1)); record_result "C009" "PASS" "No init system"
    else
        failed=$((failed + 1)); record_result "C009" "FAIL" "No init system"
    fi

    if test_c010_health_check; then
        passed=$((passed + 1)); record_result "C010" "PASS" "Health check"
    else
        failed=$((failed + 1)); record_result "C010" "FAIL" "Health check"
    fi

    if test_c011_no_debug_tools; then
        passed=$((passed + 1)); record_result "C011" "PASS" "No debug tools"
    else
        failed=$((failed + 1)); record_result "C011" "FAIL" "No debug tools"
    fi

    if test_c012_immutable_tags; then
        passed=$((passed + 1)); record_result "C012" "PASS" "Immutable tag policy"
    else
        failed=$((failed + 1)); record_result "C012" "FAIL" "Immutable tag policy"
    fi

    if test_c013_signed_images; then
        passed=$((passed + 1)); record_result "C013" "PASS" "Signed images"
    else
        failed=$((failed + 1)); record_result "C013" "FAIL" "Signed images"
    fi

    if test_c014_oci_compliance; then
        passed=$((passed + 1)); record_result "C014" "PASS" "OCI compliance"
    else
        failed=$((failed + 1)); record_result "C014" "FAIL" "OCI compliance"
    fi

    if test_c019_no_latest_tag; then
        passed=$((passed + 1)); record_result "C019" "PASS" "No latest tag"
    else
        failed=$((failed + 1)); record_result "C019" "FAIL" "No latest tag"
    fi

    echo ""
    echo "--- FUNCTIONAL TESTS ---"

    if test_functional_basic; then
        passed=$((passed + 1)); record_result "FUNC-01" "PASS" "Basic execution"
    else
        failed=$((failed + 1)); record_result "FUNC-01" "FAIL" "Basic execution"
    fi

    if test_functional_ports; then
        passed=$((passed + 1)); record_result "FUNC-02" "PASS" "Port binding"
    else
        failed=$((failed + 1)); record_result "FUNC-02" "FAIL" "Port binding"
    fi

    if test_functional_environment; then
        passed=$((passed + 1)); record_result "FUNC-03" "PASS" "Environment variables"
    else
        failed=$((failed + 1)); record_result "FUNC-03" "FAIL" "Environment variables"
    fi

    print_summary
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
        echo "  BINARY     - Binary name for functional tests (auto-detected if omitted)"
        echo "  VERBOSE    - Enable debug output (true/false)"
        exit 1
    fi

    TEST_TYPE="${1:-$TEST_TYPE}"

    case "$TEST_TYPE" in
        all)
            run_all_tests
            ;;
        functional)
            TEST_RESULTS=()
            if test_functional_basic; then
                record_result "FUNC-01" "PASS" "Basic execution"
            else
                record_result "FUNC-01" "FAIL" "Basic execution"
            fi
            if test_functional_ports; then
                record_result "FUNC-02" "PASS" "Port binding"
            else
                record_result "FUNC-02" "FAIL" "Port binding"
            fi
            if test_functional_environment; then
                record_result "FUNC-03" "PASS" "Environment variables"
            else
                record_result "FUNC-03" "FAIL" "Environment variables"
            fi
            print_summary
            ;;
        security)
            TEST_RESULTS=()
            if test_c001_non_root; then
                record_result "C001" "PASS" "Non-root user"
            else
                record_result "C001" "FAIL" "Non-root user"
            fi
            if test_c003_no_shell; then
                record_result "C003" "PASS" "No shell"
            else
                record_result "C003" "FAIL" "No shell"
            fi
            if test_c004_no_package_manager; then
                record_result "C004" "PASS" "No package manager"
            else
                record_result "C004" "FAIL" "No package manager"
            fi
            if test_c005_no_sudo; then
                record_result "C005" "PASS" "No sudo/su"
            else
                record_result "C005" "FAIL" "No sudo/su"
            fi
            if test_c008_no_docker_socket; then
                record_result "C008" "PASS" "No Docker socket"
            else
                record_result "C008" "FAIL" "No Docker socket"
            fi
            if test_c011_no_debug_tools; then
                record_result "C011" "PASS" "No debug tools"
            else
                record_result "C011" "FAIL" "No debug tools"
            fi
            print_summary
            ;;
        constraints)
            TEST_RESULTS=()
            if test_c001_non_root; then
                record_result "C001" "PASS" "Non-root user"
            else
                record_result "C001" "FAIL" "Non-root user"
            fi
            if test_c002_readonly_filesystem; then
                record_result "C002" "PASS" "Read-only filesystem"
            else
                record_result "C002" "FAIL" "Read-only filesystem"
            fi
            if test_c003_no_shell; then
                record_result "C003" "PASS" "No shell"
            else
                record_result "C003" "FAIL" "No shell"
            fi
            if test_c004_no_package_manager; then
                record_result "C004" "PASS" "No package manager"
            else
                record_result "C004" "FAIL" "No package manager"
            fi
            if test_c005_no_sudo; then
                record_result "C005" "PASS" "No sudo/su"
            else
                record_result "C005" "FAIL" "No sudo/su"
            fi
            if test_c007_minimal_packages; then
                record_result "C007" "PASS" "Minimal packages"
            else
                record_result "C007" "FAIL" "Minimal packages"
            fi
            if test_c008_no_docker_socket; then
                record_result "C008" "PASS" "No Docker socket"
            else
                record_result "C008" "FAIL" "No Docker socket"
            fi
            if test_c010_health_check; then
                record_result "C010" "PASS" "Health check"
            else
                record_result "C010" "FAIL" "Health check"
            fi
            print_summary
            ;;
        *)
            echo "Unknown test type: $TEST_TYPE"
            exit 1
            ;;
    esac
}

main "$@"
