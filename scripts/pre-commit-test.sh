#!/usr/bin/env bash
# =============================================================================
# Evergreen Image Registry - Pre-commit Fast Test Gate
# =============================================================================
# Fast pre-commit checks. Full pre-push gate runs on push.
# Exit: 0 = pass, 1 = fail
# =============================================================================
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
FAIL=0

# Gate 1: Rust clippy (fast)
if command -v cargo &>/dev/null; then
    if cargo clippy --manifest-path evergreenctl/Cargo.toml -- -D warnings 2>/dev/null; then
        echo -e "  ${GREEN}[PASS]${NC} cargo clippy"
    else
        echo -e "  ${RED}[FAIL]${NC} cargo clippy"
        FAIL=1
    fi
else
    echo "  [SKIP] cargo clippy (cargo not found)"
fi

# Gate 2: Rust fmt check
if command -v cargo &>/dev/null; then
    if cargo fmt --manifest-path evergreenctl/Cargo.toml -- --check 2>/dev/null; then
        echo -e "  ${GREEN}[PASS]${NC} cargo fmt"
    else
        echo -e "  ${RED}[FAIL]${NC} cargo fmt -- run: cargo fmt"
        FAIL=1
    fi
fi

# Gate 3: Python syntax + ruff lint (changed .py files only)
if command -v python3 &>/dev/null; then
    changed_py=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null | grep '\.py$' || true)
    if [ -n "$changed_py" ]; then
        py_fail=0
        for f in $changed_py; do
            if [ -f "$f" ]; then
                if ! python3 -m py_compile "$f" 2>/dev/null; then
                    echo -e "  ${RED}[FAIL]${NC} $f (syntax)"
                    py_fail=1
                fi
            fi
        done
        # Run ruff on changed files
        if command -v ruff &>/dev/null; then
            if ! echo "$changed_py" | xargs ruff check 2>/dev/null; then
                echo -e "  ${RED}[FAIL]${NC} ruff lint"
                py_fail=1
            fi
        fi
        if [ "$py_fail" -eq 0 ]; then
            echo -e "  ${GREEN}[PASS]${NC} Python syntax + ruff ($(echo "$changed_py" | wc -l) files)"
        else
            FAIL=1
        fi
    fi
fi

# Gate 4: Shell syntax (changed .sh files only)
changed_sh=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null | grep '\.sh$' || true)
if [ -n "$changed_sh" ]; then
    sh_fail=0
    for f in $changed_sh; do
        if [ -f "$f" ]; then
            if ! bash -n "$f" 2>/dev/null; then
                echo -e "  ${RED}[FAIL]${NC} $f"
                sh_fail=1
            fi
        fi
    done
    if [ "$sh_fail" -eq 0 ]; then
        echo -e "  ${GREEN}[PASS]${NC} Shell syntax ($(echo "$changed_sh" | wc -l) files)"
    else
        FAIL=1
    fi
fi

if [ "$FAIL" -ne 0 ]; then
    echo -e "${RED}PRE-COMMIT BLOCKED. Fix errors and retry.${NC}"
    exit 1
fi

echo -e "${GREEN}PRE-COMMIT PASSED.${NC}"
exit 0
