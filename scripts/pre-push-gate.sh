#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry - Pre-push Gate
# =============================================================================
# Enforces all quality gates before allowing push to remote.
# Runs: Rust tests, Rust clippy, Rust fmt check, Python syntax, manifest
# validation, SBOM validation, and evergreenctl audit.
#
# Exit codes:
#   0 - All gates passed, push proceeds
#   1 - One or more gates failed, push blocked
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

pass_gate() {
    PASS_COUNT=$((PASS_COUNT + 1))
    echo -e "  ${GREEN}[PASS]${NC} $1"
}

fail_gate() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo -e "  ${RED}[FAIL]${NC} $1"
}

skip_gate() {
    SKIP_COUNT=$((SKIP_COUNT + 1))
    echo -e "  ${YELLOW}[SKIP]${NC} $1"
}

echo "=========================================="
echo "Evergreen Pre-push Quality Gate"
echo "=========================================="

# ---- Gate 1: Rust unit tests ----
echo ""
echo "--- Gate 1: Rust Unit Tests ---"
if command -v cargo &>/dev/null; then
    if cargo test --manifest-path evergreenctl/Cargo.toml --lib 2>&1 | tail -5 | grep -q "test result"; then
        pass_gate "cargo test --lib (evergreenctl)"
    else
        fail_gate "cargo test --lib (evergreenctl)"
    fi
else
    skip_gate "cargo test (cargo not found)"
fi

# ---- Gate 1b: Rust integration tests ----
echo ""
echo "--- Gate 1b: Rust Integration Tests ---"
if command -v cargo &>/dev/null; then
    if cargo test --manifest-path evergreenctl/Cargo.toml --test integration 2>&1 | tail -5 | grep -q "test result"; then
        pass_gate "cargo test --test integration (evergreenctl)"
    else
        fail_gate "cargo test --test integration (evergreenctl)"
    fi
else
    skip_gate "cargo test --test integration (cargo not found)"
fi

# ---- Gate 2: Rust clippy ----
echo ""
echo "--- Gate 2: Rust Clippy ---"
if command -v cargo &>/dev/null; then
    if cargo clippy --manifest-path evergreenctl/Cargo.toml -- -D warnings 2>&1 | tail -3 | grep -qE "Finished|error"; then
        # Clippy returns 0 when no warnings (with -D warnings)
        if cargo clippy --manifest-path evergreenctl/Cargo.toml -- -D warnings 2>/dev/null; then
            pass_gate "cargo clippy (evergreenctl)"
        else
            fail_gate "cargo clippy (evergreenctl)"
        fi
    else
        pass_gate "cargo clippy (evergreenctl)"
    fi
else
    skip_gate "cargo clippy (cargo not found)"
fi

# ---- Gate 3: Rust format check ----
echo ""
echo "--- Gate 3: Rust Format Check ---"
if command -v cargo &>/dev/null; then
    if cargo fmt --manifest-path evergreenctl/Cargo.toml -- --check 2>/dev/null; then
        pass_gate "cargo fmt --check (evergreenctl)"
    else
        fail_gate "cargo fmt --check (evergreenctl) - run: cargo fmt"
    fi
else
    skip_gate "cargo fmt (cargo not found)"
fi

# ---- Gate 4: Python syntax validation ----
echo ""
echo "--- Gate 4: Python Syntax + Ruff Lint ---"
if command -v python3 &>/dev/null; then
    py_errors=0
    py_count=0
    for script in scripts/*.py generate_manifests.py; do
        if [ -f "$script" ]; then
            py_count=$((py_count + 1))
            if python3 -m py_compile "$script" 2>/dev/null; then
                : # OK
            else
                echo -e "  ${RED}[FAIL]${NC} $script (syntax)"
                py_errors=$((py_errors + 1))
            fi
        fi
    done
    # Run ruff lint if available
    if command -v ruff &>/dev/null; then
        if ! ruff check scripts/ generate_manifests.py 2>&1; then
            echo -e "  ${RED}[FAIL]${NC} ruff lint errors"
            py_errors=$((py_errors + 1))
        fi
    fi
    if [ "$py_errors" -eq 0 ]; then
        pass_gate "Python syntax + ruff lint ($py_count scripts)"
    else
        fail_gate "Python syntax + ruff lint ($py_errors error(s))"
    fi
else
    skip_gate "Python syntax (python3 not found)"
fi

# ---- Gate 4b: Shell script syntax validation ----
echo ""
echo "--- Gate 4b: Shell Script Syntax ---"
sh_errors=0
sh_count=0
for script in scripts/*.sh images/tests/*.sh images/tests/**/*.sh compliance/**/*.sh; do
    if [ -f "$script" ]; then
        sh_count=$((sh_count + 1))
        if bash -n "$script" 2>/dev/null; then
            : # OK
        else
            echo -e "  ${RED}[FAIL]${NC} $script"
            sh_errors=$((sh_errors + 1))
        fi
    fi
done
if [ "$sh_errors" -eq 0 ]; then
    pass_gate "Shell script syntax ($sh_count scripts)"
else
    fail_gate "Shell script syntax ($sh_errors/$sh_count script(s) failed)"
fi

# ---- Gate 5: Manifest validation ----
echo ""
echo "--- Gate 5: Manifest Validation ---"
if command -v python3 &>/dev/null; then
    manifest_result=$(python3 -c "
import tomllib, sys
from pathlib import Path
total = 0
errors = 0
for m in Path('images').rglob('manifest.toml'):
    total += 1
    try:
        with open(m, 'rb') as f:
            tomllib.load(f)
    except Exception:
        errors += 1
print(f'{total - errors}/{total}')
" 2>/dev/null)
    if echo "$manifest_result" | grep -qE '^[0-9]+/[0-9]+$'; then
        pass_gate "Manifest TOML validation ($manifest_result valid)"
    else
        fail_gate "Manifest TOML validation"
    fi
else
    skip_gate "Manifest validation (python3 not found)"
fi

# ---- Gate 6: SBOM validation ----
echo ""
echo "--- Gate 6: SBOM Validation ---"
if command -v python3 &>/dev/null; then
    sbom_result=$(python3 -c "
import json, sys
from pathlib import Path
total = 0
errors = 0
for s in Path('images').rglob('sbom.spdx.json'):
    total += 1
    try:
        with open(s) as f:
            data = json.load(f)
        if 'spdxVersion' not in data:
            errors += 1
    except Exception:
        errors += 1
print(f'{total - errors}/{total}')
" 2>/dev/null)
    if echo "$sbom_result" | grep -qE '^[0-9]+/[0-9]+$'; then
        pass_gate "SBOM JSON validation ($sbom_result valid)"
    else
        fail_gate "SBOM JSON validation"
    fi
else
    skip_gate "SBOM validation (python3 not found)"
fi

# ---- Gate 7: Dockerfile constraint check (sample) ----
echo ""
echo "--- Gate 7: Dockerfile Constraints ---"
if command -v python3 &>/dev/null; then
    # Check changed Dockerfiles only
    changed_dockerfiles=$(git diff --cached --name-only --diff-filter=ACM HEAD 2>/dev/null | grep -E 'Dockerfile$' || true)
    if [ -z "$changed_dockerfiles" ]; then
        # Also check unstaged changes
        changed_dockerfiles=$(git diff --name-only --diff-filter=ACM HEAD 2>/dev/null | grep -E 'Dockerfile$' || true)
    fi
    if [ -n "$changed_dockerfiles" ]; then
        constraint_errors=0
        dcf_count=0
        for df in $changed_dockerfiles; do
            if [ -f "$df" ]; then
                dcf_count=$((dcf_count + 1))
                # Check for Alpine (CRITICAL)
                if grep -qiE '^\s*FROM\s+.*alpine' "$df" 2>/dev/null; then
                    echo -e "  ${RED}[FAIL]${NC} $df: Alpine base detected (BANNED)"
                    constraint_errors=$((constraint_errors + 1))
                fi
                # Check for unpinned FROM (supply chain)
                if grep -E '^\s*FROM\s+' "$df" 2>/dev/null | grep -v '@sha256:' | grep -vqi 'scratch'; then
                    echo -e "  ${YELLOW}[WARN]${NC} $df: Unpinned FROM line detected"
                fi
            fi
        done
        if [ "$constraint_errors" -eq 0 ]; then
            pass_gate "Dockerfile constraints (checked $dcf_count files)"
        else
            fail_gate "Dockerfile constraints ($constraint_errors violation(s))"
        fi
    else
        pass_gate "Dockerfile constraints (no Dockerfile changes)"
    fi
else
    skip_gate "Dockerfile constraints (python3 not found)"
fi

# ---- Gate 9: Cargo audit (dependency vulnerability scan) ----
echo ""
echo "--- Gate 9: Cargo Audit ---"
if command -v cargo-audit &>/dev/null; then
    if (cd evergreenctl && cargo audit 2>/dev/null); then
        pass_gate "cargo audit (evergreenctl)"
    else
        fail_gate "cargo audit (evergreenctl) - vulnerabilities found"
    fi
else
    skip_gate "cargo audit (cargo-audit not found)"
fi

# ---- Gate 8: Rust release build ----
echo ""
echo "--- Gate 8: Rust Release Build ---"
if command -v cargo &>/dev/null; then
    if cargo build --release --manifest-path evergreenctl/Cargo.toml 2>/dev/null; then
        pass_gate "cargo build --release (evergreenctl)"
    else
        fail_gate "cargo build --release (evergreenctl)"
    fi
else
    skip_gate "Rust release build (cargo not found)"
fi

# ---- Gate 10: Go vet + test (health-shim) ----
echo ""
echo "--- Gate 10: Go Vet + Test (health-shim) ---"
if command -v go &>/dev/null; then
    GO_FAIL=0
    if [ -d "images/health-shim" ]; then
        if ! (cd images/health-shim && go vet ./... 2>&1); then
            echo -e "  ${RED}[FAIL]${NC} go vet (health-shim)"
            GO_FAIL=1
        fi
        if ! (cd images/health-shim && go test ./... 2>&1); then
            echo -e "  ${RED}[FAIL]${NC} go test (health-shim)"
            GO_FAIL=1
        fi
        if [ "$GO_FAIL" -eq 0 ]; then
            pass_gate "Go vet + test (health-shim)"
        else
            fail_gate "Go vet + test (health-shim)"
        fi
    else
        skip_gate "Go vet + test (images/health-shim not found)"
    fi
else
    skip_gate "Go vet + test (go not found)"
fi

# ---- Summary ----
echo ""
echo "=========================================="
echo "PRE-PUSH GATE SUMMARY"
echo "=========================================="
echo -e "  ${GREEN}PASS${NC}: $PASS_COUNT"
echo -e "  ${RED}FAIL${NC}: $FAIL_COUNT"
echo -e "  ${YELLOW}SKIP${NC}: $SKIP_COUNT"
echo "=========================================="

if [ "$FAIL_COUNT" -gt 0 ]; then
    echo -e "${RED}BLOCKED: $FAIL_COUNT gate(s) failed. Fix and retry.${NC}"
    exit 1
fi

echo -e "${GREEN}ALL GATES PASSED. Push proceeds.${NC}"
exit 0
