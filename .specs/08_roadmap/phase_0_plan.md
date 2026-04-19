# =============================================================================
# PHASE 0: FIX THE FOUNDATION - Detailed Execution Plan
# =============================================================================
# Version: 1.0.0
# Status: IN_PROGRESS
# Author: Nexus (Principal Systems Architect)
# Date: 2026-04-19
#
# ABSTRACT: This phase addresses all critical infrastructure issues that
# prevent reliable builds, testing, and verification. The current state
# has been audited and 10 critical issues identified. This plan addresses
# each with specific steps, verification criteria, and rollback procedures.
# =============================================================================

## Table of Contents

1. [Current State Assessment](#1-current-state-assessment)
2. [Task Inventory](#2-task-inventory)
3. [Detailed Task Specifications](#3-detailed-task-specifications)
4. [Quality Gates](#4-quality-gates)
5. [Risk Register](#5-risk-register)
6. [Rollback Procedures](#6-rollback-procedures)
7. [Success Metrics](#7-success-metrics)

---

## 1. Current State Assessment

### 1.1 Image Category Distribution

| Category | Count | Percentage | Base Image | HEALTHCHECK Status |
|----------|-------|------------|------------|-------------------|
| A: Scratch | 104 | 46.6% | `FROM scratch` | **ALL BROKEN** (shell form in no-shell image) |
| B: Distroless | 7 | 3.1% | `gcr.io/distroless/*` | **ALL BROKEN** (shell form in no-shell image) |
| C: Wolfi | 13 | 5.8% | `cgr.dev/chainguard/wolfi-base:latest` | Mostly broken (bad CMD patterns) |
| D: Debian-slim | 87 | 39.0% | `debian:bookworm-slim` | Mostly broken (two-word CMD bug) |
| E: Other/Official | 12 | 5.4% | Various official | Missing or broken |
| **TOTAL** | **223** | **100%** | | **~180 BROKEN** |

### 1.2 Critical Issues Summary

| ID | Issue | Severity | Images Affected | Root Cause |
|----|-------|----------|-----------------|------------|
| CI-001 | build.yml typo `/temp/` vs `/tmp/` | CRITICAL | All | Typo on line 247 |
| CI-002 | GHA matrix truncation | CRITICAL | All | 223-image matrix exceeds limits |
| CI-003 | Lint stage disabled | HIGH | All | Commented out |
| HC-001 | Shell-form HEALTHCHECK in scratch | CRITICAL | 104 | Template generation bug |
| HC-002 | Shell-form HEALTHCHECK in distroless | CRITICAL | 7 | Template generation bug |
| HC-003 | Two-word CMD pattern bug | HIGH | ~70 | Template logic error |
| PKG-001 | Package manager in final image | CRITICAL | 87 | Single-stage debian-slim |
| SHL-001 | Shell in final image | CRITICAL | 87 | Inherited from debian-slim |
| TST-001 | Test framework arithmetic bug | HIGH | All | `((failed++)) || ((passed++))` pattern |
| VER-001 | Unpinned base image tags | HIGH | 13 | `:latest` in wolfi images |

### 1.3 Supply Chain Issues (Deferred to Phase 1)

| ID | Issue | Severity | Images Affected |
|----|-------|----------|-----------------|
| SC-001 | No checksum verification | CRITICAL | 124 (all multi-stage) |
| SC-002 | No SLSA provenance | HIGH | All |
| SC-003 | Insecure Cosign signing | HIGH | All |
| SC-004 | No secret scanning | HIGH | All |

---

## 2. Task Inventory

### Dependency Graph (Topological Order)

```
T0.0.1 (Roadmap docs) ─────┬──> T0.0.2 (ADR: HEALTHCHECK) ────> T0.2.1-T0.2.4
                           ├──> T0.0.3 (ADR: Checksum)  ──────> Phase 1
                           └──> T0.0.4 (ADR: Multistage) ───> T0.3.1

T0.1.1 (Fix typo) ──> T0.1.2 (Fix matrix) ──> T0.1.3 (Enable lint)
                                                 └──> T0.6.1 (Multi-arch)

T0.4.1 (Fix tests) ──> T0.4.2 (Expand test config)

T0.5.1 (Pin tags) ──> Independent

T0.3.1 (Convert debian) ──> T0.2.4 (Fix debian HEALTHCHECK)
```

### Parallel Execution Opportunities

```
Stream A: Documentation (T0.0.1 → T0.0.2/3/4)
Stream B: CI Fixes (T0.1.1 → T0.1.2 → T0.1.3, T0.6.1)
Stream C: Dockerfile Fixes (T0.5.1, T0.4.1 → T0.4.2)
Stream D: HEALTHCHECK Fixes (after T0.0.2: T0.2.1, T0.2.2, T0.2.3, T0.2.4)
Stream E: Multi-stage Conversion (after T0.0.4: T0.3.1)
```

---

## 3. Detailed Task Specifications

### 3.1 T0.2.1: Fix HEALTHCHECK for Category A (104 scratch images)

#### Problem Analysis

Every scratch image has a HEALTHCHECK like:
```dockerfile
HEALTHCHECK CMD nginx -v
```

This is **shell form** — Docker wraps it as `/bin/sh -c "nginx -v"`. Since `FROM scratch` has no `/bin/sh`, this **always fails** with:
```
OCI runtime exec failed: exec failed: unable to start container process: exec: "/bin/sh": stat /bin/sh: no such file or directory
```

Additionally, even if we switched to exec form, `CMD nginx -v` would be interpreted by the shell as running `nginx` with argument `-v`, but since ENTRYPOINT is `["/nginx"]`, the HEALTHCHECK CMD is **appended to ENTRYPOINT**, resulting in `/nginx nginx -v` — which is wrong.

#### Solution: Exec-Form HEALTHCHECK with Absolute Path

**For scratch images, the HEALTHCHECK must:**
1. Use exec form: `CMD ["/binary", "arg1", "arg2"]`
2. Use absolute path (no PATH in scratch)
3. NOT depend on ENTRYPOINT (use a separate CMD, not appended)
4. Use a binary that exists in the scratch image

**Pattern for binary-only health checks:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/nginx", "-v"]
```

This runs `/nginx -v` directly, bypassing the ENTRYPOINT.

**Pattern for HTTP health checks (requires embedding a health checker):**
For images that serve HTTP but have no curl/wget, we need to either:
- Copy a static `wget` or `curl` binary from the downloader stage
- Accept that HTTP health checks are not possible in pure scratch

**Decision:** For Phase 0, use binary version checks. HTTP health checks will be added in Phase 2 by embedding a minimal static `wget` binary.

#### Migration Script Logic

```python
# For each scratch-based Dockerfile:
# 1. Find HEALTHCHECK line
# 2. Extract binary name from ENTRYPOINT (first element of JSON array)
# 3. Determine version flag (--version, -v, version)
# 4. Replace with: CMD ["/binary", "--version"]
```

#### Verification

```bash
# Test that HEALTHCHECK doesn't require shell
docker inspect <image> --format='{{.Config.Healthcheck.Test}}'
# Expected: ["/nginx", "-v"]
# NOT expected: ["CMD-SHELL", "nginx -v"]
```

### 3.2 T0.2.4: Fix HEALTHCHECK for Category D (87 debian-slim images)

#### Problem Analysis

Most debian-slim images have:
```dockerfile
HEALTHCHECK CMD python curl -s localhost:8080/api/status
```

In shell form, this runs `python` with arguments `curl -s localhost:8080/api/status`. This is wrong — it should run `curl` directly.

#### Corrected Pattern

```dockerfile
# Before (WRONG):
HEALTHCHECK CMD python curl -s localhost:8080/api/status

# After (CORRECT - for images with curl installed):
HEALTHCHECK CMD curl -sf http://localhost:8080/api/status || exit 1

# After (CORRECT - for images without curl, use wget):
HEALTHCHECK CMD wget -qO- http://localhost:8080/api/status || exit 1

# After (CORRECT - for simple binary checks):
HEALTHCHECK CMD pg_isready -h localhost
```

#### Migration Strategy

| Sub-pattern | Count | Fix |
|-------------|-------|-----|
| `CMD <binary> <healthcheck-binary>` (two-word) | ~70 | Remove first binary, keep healthcheck command |
| `CMD <single-healthcheck-command>` | ~10 | Already correct, verify |
| `CMD curl -s ... \|\| exit 1` | ~7 | Add `-sf` flags for silent+fail-on-error |

### 3.3 T0.3.1: Convert debian-slim images to multi-stage scratch builds

#### Analysis

Of the 87 debian-slim images, some CAN be converted to multi-stage (download binary → copy to scratch) and some CANNOT (they genuinely need the OS runtime).

#### Conversion Decision Matrix

| Criterion | Can Convert to Scratch | Must Stay Multi-OS |
|-----------|----------------------|-------------------|
| Binary distributed as static | YES | - |
| Binary distributed as dynamic (needs glibc) | Maybe (use distroless/cc) | NO (needs full OS) |
| Requires system packages (python, php, node) | NO | YES |
| Requires shared libraries (.so files) | Maybe (bundle in scratch) | YES |
| Requires OS services (systemd, syslog) | NO | YES |

#### Estimated Conversion Results

| Category | Estimated Count | Target Base |
|----------|----------------|-------------|
| Static binaries available | ~20 | `FROM scratch` |
| Dynamic but can bundle | ~15 | `FROM scratch` (bundle .so) |
| Need glibc runtime | ~10 | `FROM gcr.io/distroless/cc-debian12` |
| Need full OS (python, php, node, java) | ~42 | Stay `debian:bookworm-slim` but multi-stage |

**For images that must stay debian-slim:**
- Convert to multi-stage: install packages in builder, copy only needed files to final stage
- Remove apt lists, documentation, man pages
- Remove shell if possible (depends on runtime needs)
- Create dedicated non-root user

### 3.4 T0.1.2: Fix GHA Matrix Truncation

#### Problem

GitHub Actions has a 256-job limit per workflow run. With 223 images, the matrix is near this limit. Additionally, the `discover` step output may exceed GHA's output size limit.

#### Solution: Batched Matrix Strategy

```yaml
# Split into 3 batches of ~75 images each
strategy:
  matrix:
    batch: [1, 2, 3]
    # Each batch builds ~75 images
```

Alternative: Use a single reusable workflow that processes images from a queue artifact.

### 3.5 T0.4.1: Fix Test Framework Arithmetic

#### Problem

```bash
test_c001_non_root || ((failed++)) || ((passed++))
```

When `test_c001_non_root` fails (exit 1):
1. `|| ((failed++))` fires: `failed` becomes 1, but `((failed++))` evaluates `failed` (which was 0), returns exit code 1 (falsy in bash arithmetic)
2. `|| ((passed++))` fires because previous `||` chain got exit code 1: `passed` becomes 1

**Result:** Both `failed` and `passed` are incremented. Test results are unreliable.

#### Fix

```bash
if test_c001_non_root; then
    ((passed++))
else
    ((failed++))
fi
```

---

## 4. Quality Gates

### Gate QG-0.1: CI Pipeline Builds All Images

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| Build success rate | Jobs passed / Jobs total | 100% |
| Build time (average) | Mean build duration | < 5 minutes |
| Matrix coverage | Images built / Total images | 100% |

### Gate QG-0.2: HEALTHCHECK Works

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| Exec form usage | Images with exec-form HEALTHCHECK / Total | 100% |
| Absolute path | Images using absolute path in HEALTHCHECK | 100% for scratch/distroless |
| Manual verification | Images manually tested | 100% of Tier 1 |

### Gate QG-0.3: No Unpinned Tags

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| Latest tag count | `grep -c ':latest'` | 0 |

### Gate QG-0.4: Test Framework Correctness

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| Pass count accuracy | Known-good image shows 0 failures | Exact |
| Fail count accuracy | Known-bad image shows correct failures | Exact |

---

## 5. Risk Register

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| Some images cannot be converted to scratch | HIGH | MEDIUM | Document exceptions in ADR-003 | Nexus |
| HEALTHCHECK exec form breaks for complex binaries | LOW | MEDIUM | Fallback to version-check pattern | Nexus |
| GHA matrix still truncates after batching | LOW | HIGH | Switch to reusable workflow dispatch | Nexus |
| Base image version pin becomes stale | MEDIUM | LOW | Dependabot + manual review | Nexus |
| Test config entries are wrong | MEDIUM | MEDIUM | Validate against Dockerfile analysis | Nexus |

---

## 6. Rollback Procedures

### If T0.3.1 (multi-stage conversion) causes widespread failures:
1. Revert to single-stage debian-slim for affected images
2. Document failures in ADR-003
3. Create GitHub issues for manual investigation

### If T0.1.2 (matrix batching) causes CI instability:
1. Revert to single batch with reduced image set
2. Implement queue-based approach in next iteration

---

## 7. Success Metrics

| Metric | Current Value | Target Value | Measurement |
|--------|--------------|--------------|-------------|
| Images with working HEALTHCHECK | ~43 (19%) | 223 (100%) | `docker inspect` check |
| Images passing C003 (no shell) | 104 (47%) | 180+ (81%) | Container test |
| Images passing C004 (no pkg mgr) | 104 (47%) | 180+ (81%) | Container test |
| CI pipeline success rate | 0% | 100% | GitHub Actions |
| Test framework accuracy | ~50% | 100% | Known-good/bad test |
| Images with pinned base tags | 210 (94%) | 223 (100%) | Grep check |

---

**END OF PHASE 0 PLAN**
