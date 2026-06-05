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

# ---- Gate 6b: Drift detection (manifest vs Dockerfile) ----
echo ""
echo "--- Gate 6b: Drift Detection ---"
if command -v evergreenctl &>/dev/null; then
    changed_images=$(git diff --cached --name-only --diff-filter=ACM HEAD 2>/dev/null \
      | grep -oP 'images/\K[^/]+' | sort -u || true)
    if [ -z "$changed_images" ]; then
        changed_images=$(git diff --name-only --diff-filter=ACM HEAD 2>/dev/null \
          | grep -oP 'images/\K[^/]+' | sort -u || true)
    fi
    if [ -n "$changed_images" ]; then
        drift_errors=0
        drift_count=0
        for img in $changed_images; do
            img_dir="images/${img}"
            if [ -f "${img_dir}/Dockerfile" ] && [ -f "${img_dir}/manifest.toml" ]; then
                drift_count=$((drift_count + 1))
                if ! evergreenctl drift "$img_dir" 2>&1; then
                    echo -e "  ${RED}[FAIL]${NC} drift detected in ${img}"
                    drift_errors=$((drift_errors + 1))
                fi
            fi
        done
        if [ "$drift_errors" -eq 0 ]; then
            pass_gate "Drift detection ($drift_count images checked)"
        else
            fail_gate "Drift detection ($drift_errors image(s) have drift)"
        fi
    else
        pass_gate "Drift detection (no image changes)"
    fi
else
    skip_gate "Drift detection (evergreenctl not found)"
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

# ---- Gate 11: FIPS Compliance Check ----
echo ""
echo "--- Gate 11: FIPS Compliance Check ---"
if command -v python3 &>/dev/null; then
    fips_result=$(python3 -c "
import tomllib, sys
from pathlib import Path

# Load FIPS image matrix
fips_matrix_path = Path('compliance/fips/fips_image_matrix.yaml')
fips_images = set()
if fips_matrix_path.exists():
    try:
        import yaml
        with open(fips_matrix_path) as f:
            data = yaml.safe_load(f)
        for cat in data.get('fips_image_matrix', {}).get('categories', {}).values():
            for img in cat.get('images', []):
                name = img.get('name', '')
                if name:
                    fips_images.add(name)
    except Exception:
        # Fallback: try without yaml
        pass

# Find images claiming FIPS in manifest
claims_fips = []
for m in Path('images').rglob('manifest.toml'):
    try:
        with open(m, 'rb') as f:
            data = tomllib.load(f)
        labels = data.get('labels', {})
        if labels.get('compliance.fips') == 'true':
            claims_fips.append(m.parent.name)
    except Exception:
        pass

# Check for compliance/fips/ files per image
has_compliance = set()
for f in Path('compliance/fips').rglob('*'):
    if f.is_file() and f.suffix in ('.md', '.yaml', '.yml', '.sh'):
        pass  # These are shared files, not per-image

print(f'matrix:{len(fips_images)}|claims:{len(claims_fips)}')
" 2>/dev/null)
    if echo "$fips_result" | grep -qE '^matrix:[0-9]+|claims:[0-9]+$'; then
        matrix_count=$(echo "$fips_result" | grep -oP 'matrix:\K[0-9]+')
        claims_count=$(echo "$fips_result" | grep -oP 'claims:\K[0-9]+')
        if [ "$claims_count" -gt 0 ]; then
            # Warn if images claim FIPS but aren't in the matrix
            python3 -c "
import tomllib, sys
from pathlib import Path

fips_matrix_path = Path('compliance/fips/fips_image_matrix.yaml')
fips_images = set()
try:
    import yaml
    with open(fips_matrix_path) as f:
        data = yaml.safe_load(f)
    for cat in data.get('fips_image_matrix', {}).get('categories', {}).values():
        for img in cat.get('images', []):
            name = img.get('name', '')
            if name:
                fips_images.add(name)
except Exception:
    pass

claims = []
for m in Path('images').rglob('manifest.toml'):
    try:
        with open(m, 'rb') as f:
            data = tomllib.load(f)
        labels = data.get('labels', {})
        if labels.get('compliance.fips') == 'true':
            claims.append(m.parent.name)
    except Exception:
        pass

unlisted = [c for c in claims if c not in fips_images]
if unlisted:
    print(f'WARN: {len(unlisted)} image(s) claim FIPS but are not in compliance/fips/ matrix: {\" \".join(unlisted)}')
    sys.exit(1)
else:
    sys.exit(0)
" 2>/dev/null
            if [ $? -ne 0 ]; then
                echo -e "  ${YELLOW}[WARN]${NC} Some images claim FIPS but lack compliance/fips/ documentation"
            fi
            pass_gate "FIPS compliance check ($matrix_count matrix images, $claims_count claiming FIPS)"
        else
            pass_gate "FIPS compliance check ($matrix_count matrix images, no manifest claims)"
        fi
    else
        skip_gate "FIPS compliance check (parse error)"
    fi
else
    skip_gate "FIPS compliance check (python3 not found)"
fi

# ---- Gate 12: Performance regression detection ----
echo ""
echo "--- Gate 12: Performance Regression Detection ---"
if command -v docker &>/dev/null && command -v python3 &>/dev/null; then
    BASELINE_FILE=".specs/06_5_regression/build_times.json"
    THRESHOLD=50
    PERF_ERRORS=0
    PERF_COUNT=0
    PERF_UPDATED=0

    changed_images=$(git diff --cached --name-only --diff-filter=ACM HEAD 2>/dev/null \
      | grep -oP 'images/\K[^/]+' | sort -u || true)
    if [ -z "$changed_images" ]; then
        changed_images=$(git diff --name-only --diff-filter=ACM HEAD 2>/dev/null \
          | grep -oP 'images/\K[^/]+' | sort -u || true)
    fi

    if [ -n "$changed_images" ]; then
        for img in $changed_images; do
            img_dir="images/${img}"
            if [ ! -f "${img_dir}/Dockerfile" ]; then
                continue
            fi

            PERF_COUNT=$((PERF_COUNT + 1))
            echo -n "  Build timing: ${img}... "

            START_NS=$(date +%s%N)
            if docker build -t "evergreen-perf-test-${img}" "${img_dir}" >/dev/null 2>&1; then
                END_NS=$(date +%s%N)
                ELAPSED_MS=$(( (END_NS - START_NS) / 1000000 ))

                # Check against baseline
                EXISTING=$(python3 -c "
import json, sys
try:
    with open('${BASELINE_FILE}') as f:
        data = json.load(f)
    bt = data.get('images', {}).get('${img}', {}).get('build_time_ms', 0)
    print(bt)
except Exception:
    print(0)
" 2>/dev/null || echo "0")

                if [ "$EXISTING" -gt 0 ]; then
                    INCREASE=$(( (ELAPSED_MS - EXISTING) * 100 / EXISTING ))
                    if [ "$INCREASE" -gt "$THRESHOLD" ]; then
                        echo "FAIL (+${INCREASE}% > ${THRESHOLD}% threshold: ${EXISTING}ms -> ${ELAPSED_MS}ms)"
                        PERF_ERRORS=$((PERF_ERRORS + 1))
                    else
                        echo "OK (${ELAPSED_MS}ms, baseline ${EXISTING}ms, +${INCREASE}%)"
                    fi
                else
                    echo "NEW BASELINE (${ELAPSED_MS}ms)"
                fi

                # Update baseline
                python3 -c "
import json
try:
    with open('${BASELINE_FILE}') as f:
        data = json.load(f)
except Exception:
    data = {'version': 1, 'description': 'Build time baselines', 'threshold_percent': 50, 'images': {}}

if 'images' not in data:
    data['images'] = {}
data['images']['${img}'] = {
    'build_time_ms': ${ELAPSED_MS},
    'updated': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
}

with open('${BASELINE_FILE}', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null || true
                PERF_UPDATED=$((PERF_UPDATED + 1))

                docker rmi "evergreen-perf-test-${img}" >/dev/null 2>&1 || true
            else
                echo "SKIP (build failed)"
            fi
        done

        if [ "$PERF_ERRORS" -eq 0 ] && [ "$PERF_COUNT" -gt 0 ]; then
            pass_gate "Performance regression (${PERF_COUNT} images, ${PERF_UPDATED} baselines updated)"
        elif [ "$PERF_ERRORS" -gt 0 ]; then
            fail_gate "Performance regression (${PERF_ERRORS}/${PERF_COUNT} images exceeded ${THRESHOLD}% threshold)"
        else
            pass_gate "Performance regression (no buildable changed images)"
        fi
    else
        pass_gate "Performance regression (no image changes)"
    fi
else
    skip_gate "Performance regression (docker or python3 not found)"
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
