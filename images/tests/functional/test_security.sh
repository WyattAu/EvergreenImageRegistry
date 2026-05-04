#!/bin/bash
# =============================================================================
# FUNCTIONAL TEST SUITE - SECURITY TOOLS
# =============================================================================
# Tests for security tool images: Vault, Trivy, Cosign, Grype
#
# Usage: IMAGE=<image> ./test_security.sh
#        ./test_security.sh <image>
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

detect_security_type() {
    local img="$1"
    case "$img" in
        *vault*) echo "vault" ;;
        *trivy*) echo "trivy" ;;
        *cosign*) echo "cosign" ;;
        *grype*) echo "grype" ;;
        *syft*) echo "syft" ;;
        *step-cli*|*step*) echo "step-cli" ;;
        *fail2ban*) echo "fail2ban" ;;
        *modsecurity*) echo "modsecurity" ;;
        *oauth2-proxy*) echo "oauth2-proxy" ;;
        *keycloak*|*dex*|*zitadel*|*authelia*|*headscale*) echo "identity" ;;
        *) echo "unknown" ;;
    esac
}

# =============================================================================
# VAULT TESTS
# =============================================================================

test_vault() {
    echo ""
    echo "--- Vault Tests ---"

    CONTAINER_NAME="sectest-vault-$(date +%s)-$$"
    if ! docker run -d \
        --name "$CONTAINER_NAME" \
        -e VAULT_DEV_ROOT_TOKEN_ID=root \
        -p 18200:8200 \
        "$IMAGE" server -dev >/dev/null 2>&1; then
        record "VAULT-START" "FAIL" "Container failed to start"
        return
    fi

    if ! wait_for_container 15; then
        record "VAULT-START" "FAIL" "Container did not become ready within timeout"
        docker logs "$CONTAINER_NAME" 2>&1 | tail -5
        return
    fi
    record "VAULT-START" "PASS" "Container started in dev mode"

    if command -v curl &>/dev/null; then
        local seal_status
        seal_status=$(curl -sf --max-time 5 -H "X-Vault-Token: root" "http://127.0.0.1:18200/v1/sys/seal-status" 2>/dev/null || echo "")
        if echo "$seal_status" | grep -q '"sealed":false'; then
            record "VAULT-UNSEAL" "PASS" "Vault is unsealed"
        else
            record "VAULT-UNSEAL" "SKIP" "Could not verify seal status"
        fi

        local write_result
        write_result=$(curl -sf --max-time 5 -X PUT \
            -H "X-Vault-Token: root" \
            -d '{"data":{"value":"secret123"}}' \
            "http://127.0.0.1:18200/v1/secret/data/test" 2>/dev/null || echo "")
        if [ -n "$write_result" ]; then
            record "VAULT-WRITE" "PASS" "Write secret succeeded"
        else
            record "VAULT-WRITE" "FAIL" "Write secret failed"
        fi

        local read_result
        read_result=$(curl -sf --max-time 5 -H "X-Vault-Token: root" \
            "http://127.0.0.1:18200/v1/secret/data/test" 2>/dev/null || echo "")
        if echo "$read_result" | grep -q "secret123"; then
            record "VAULT-READ" "PASS" "Read secret returned correct value"
        else
            record "VAULT-READ" "FAIL" "Read secret did not return expected value"
        fi
    else
        record "VAULT-UNSEAL" "SKIP" "curl not available"
        record "VAULT-WRITE" "SKIP" "curl not available"
        record "VAULT-READ" "SKIP" "curl not available"
    fi

    docker kill "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    CONTAINER_NAME=""
}

# =============================================================================
# TRIVY TESTS
# =============================================================================

test_trivy() {
    echo ""
    echo "--- Trivy Tests ---"

    local version_output
    version_output=$(docker run --rm "$IMAGE" version 2>&1 || echo "")
    if echo "$version_output" | grep -qE "Version|version"; then
        record "TRIVY-VERSION" "PASS" "Trivy version command succeeded"
        echo "    Output: $(echo "$version_output" | head -3)"
    else
        record "TRIVY-VERSION" "FAIL" "Trivy version command failed: $version_output"
        return
    fi

    local help_output
    help_output=$(docker run --rm "$IMAGE" --help 2>&1 || echo "")
    if echo "$help_output" | grep -qiE "image|scan|fs"; then
        record "TRIVY-HELP" "PASS" "Trivy help shows scan capabilities"
    else
        record "TRIVY-HELP" "FAIL" "Trivy help output unexpected"
    fi

    record "TRIVY-SCAN" "SKIP" "Full image scan skipped (requires target image)"
}

# =============================================================================
# COSIGN TESTS
# =============================================================================

test_cosign() {
    echo ""
    echo "--- Cosign Tests ---"

    local version_output
    version_output=$(docker run --rm "$IMAGE" version 2>&1 || echo "")
    if echo "$version_output" | grep -qE "Version|version|GitVersion|v[0-9]"; then
        record "COSIGN-VERSION" "PASS" "Cosign version command succeeded"
        echo "    Output: $(echo "$version_output" | head -3)"
    else
        record "COSIGN-VERSION" "FAIL" "Cosign version command failed: $version_output"
        return
    fi

    local help_output
    help_output=$(docker run --rm "$IMAGE" --help 2>&1 || echo "")
    if echo "$help_output" | grep -qiE "verify|sign|download"; then
        record "COSIGN-HELP" "PASS" "Cosign help shows verify/sign capabilities"
    else
        record "COSIGN-HELP" "FAIL" "Cosign help output unexpected"
    fi

    record "COSIGN-VERIFY" "SKIP" "Full signature verification skipped (requires signed image)"
}

# =============================================================================
# GRYPE TESTS
# =============================================================================

test_grype() {
    echo ""
    echo "--- Grype Tests ---"

    local version_output
    version_output=$(docker run --rm "$IMAGE" version 2>&1 || echo "")
    if echo "$version_output" | grep -qE "Version|version|v[0-9]"; then
        record "GRYPE-VERSION" "PASS" "Grype version command succeeded"
        echo "    Output: $(echo "$version_output" | head -3)"
    else
        record "GRYPE-VERSION" "FAIL" "Grype version command failed: $version_output"
        return
    fi

    local help_output
    help_output=$(docker run --rm "$IMAGE" --help 2>&1 || echo "")
    if echo "$help_output" | grep -qiE "scan|db|vulnerability"; then
        record "GRYPE-HELP" "PASS" "Grype help shows scan capabilities"
    else
        record "GRYPE-HELP" "FAIL" "Grype help output unexpected"
    fi

    record "GRYPE-SCAN" "SKIP" "Full vulnerability scan skipped (requires target image)"
}

# =============================================================================
# SYFT TESTS
# =============================================================================

test_syft() {
    echo ""
    echo "--- Syft Tests ---"

    local version_output
    version_output=$(docker run --rm "$IMAGE" version 2>&1 || echo "")
    if echo "$version_output" | grep -qE "Version|version|v[0-9]"; then
        record "SYFT-VERSION" "PASS" "Syft version command succeeded"
        echo "    Output: $(echo "$version_output" | head -3)"
    else
        record "SYFT-VERSION" "FAIL" "Syft version command failed: $version_output"
        return
    fi

    local help_output
    help_output=$(docker run --rm "$IMAGE" --help 2>&1 || echo "")
    if echo "$help_output" | grep -qiE "scan|sbom|packages"; then
        record "SYFT-HELP" "PASS" "Syft help shows SBOM scan capabilities"
    else
        record "SYFT-HELP" "FAIL" "Syft help output unexpected"
    fi

    record "SYFT-SCAN" "SKIP" "Full SBOM generation skipped (requires target image)"
}

# =============================================================================
# STEP-CLI TESTS
# =============================================================================

test_step_cli() {
    echo ""
    echo "--- Step-CLI Tests ---"

    local version_output
    version_output=$(docker run --rm "$IMAGE" version 2>&1 || echo "")
    if echo "$version_output" | grep -qE "Version|version|v[0-9]|Smallstep"; then
        record "STEP-VERSION" "PASS" "Step CLI version command succeeded"
        echo "    Output: $(echo "$version_output" | head -3)"
    else
        record "STEP-VERSION" "FAIL" "Step CLI version command failed: $version_output"
        return
    fi

    local help_output
    help_output=$(docker run --rm "$IMAGE" --help 2>&1 || echo "")
    if echo "$help_output" | grep -qiE "certificate|ca|crypto"; then
        record "STEP-HELP" "PASS" "Step CLI help shows certificate/crypto capabilities"
    else
        record "STEP-HELP" "FAIL" "Step CLI help output unexpected"
    fi
}

# =============================================================================
# GENERIC SECURITY TOOL TEST (fallback)
# =============================================================================

test_generic_security() {
    echo ""
    echo "--- Generic Security Tool Test ---"

    local entrypoint
    entrypoint=$(docker inspect "$IMAGE" --format='{{(index .Config.Entrypoint 0)}}' 2>/dev/null || echo "")
    local cmd0
    cmd0=$(docker inspect "$IMAGE" --format='{{(index .Config.Cmd 0)}}' 2>/dev/null || echo "")
    local binary="${entrypoint:-$cmd0}"

    if [ -n "$binary" ] && [ "$binary" != "null" ] && [ "$binary" != "<no value>" ]; then
        local version_output
        version_output=$(docker run --rm "$IMAGE" --version 2>&1 || docker run --rm "$IMAGE" -v 2>&1 || docker run --rm "$IMAGE" version 2>&1 || echo "")
        if [ -n "$version_output" ] && [ "$version_output" != "" ]; then
            record "GENSEC-VERSION" "PASS" "Binary $binary responds to version flag"
            echo "    Output: $(echo "$version_output" | head -3)"
        else
            record "GENSEC-VERSION" "SKIP" "Binary $binary did not respond to version flags"
        fi
    else
        record "GENSEC-VERSION" "SKIP" "No binary detected"
    fi
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
    echo "SECURITY TOOL FUNCTIONAL TESTS"
    echo "Image: $IMAGE"
    echo "=========================================="

    local sec_type
    sec_type=$(detect_security_type "$IMAGE")
    echo "Detected security tool type: $sec_type"

    case "$sec_type" in
        vault) test_vault ;;
        trivy) test_trivy ;;
        cosign) test_cosign ;;
        grype) test_grype ;;
        syft) test_syft ;;
        step-cli) test_step_cli ;;
        *) test_generic_security ;;
    esac

    echo ""
    echo "=========================================="
    echo "SUMMARY: $IMAGE (type=$sec_type)"
    echo "=========================================="
    echo -e "  ${GREEN}PASS${NC}: $PASS_COUNT"
    echo -e "  ${RED}FAIL${NC}: $FAIL_COUNT"
    echo -e "  ${YELLOW}SKIP${NC}: $SKIP_COUNT"
    echo "  TOTAL: $TOTAL"
    echo "=========================================="

    [ $FAIL_COUNT -eq 0 ]
}

main "$@"
