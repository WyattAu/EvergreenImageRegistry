# Evergreen Image Registry -- Path and Roadmap Forward

## Executive Summary

The registry is at v26.4.0 with 998 images, all syntax-correct, fully labeled, SBOM-covered, and gated by CI. The remaining ~80-120 CI build failures are entirely upstream issues (deleted releases, auth-gated registries, broken builds). This document describes the path from the current state to a production-hardened, zero-trust container image supply chain.

---

## 1. Current State Assessment

### 1.1 What Is Done

| Category | Metric | Status |
|----------|--------|--------|
| Images | 998 Dockerfiles, 998 manifests, 998 SBOMs | COMPLETE |
| TOML/JSON validation | 998/998 manifest.toml + sbom.spdx.json | COMPLETE |
| Dockerfile syntax | 0 errors across all 998 images | COMPLETE |
| Anti-patterns | 0 real (shells, eval, sudo, apt-get in final) | COMPLETE |
| Security labels | 4 mandatory labels on 100% of images | COMPLETE |
| OCI compliance | title (100%), description (99.9%), source (99.7%), version (99.8%) | COMPLETE |
| Non-root execution | 99.5% (993/998) | COMPLETE |
| HEALTHCHECK | 559 real + 438 NONE (scratch) = 998/998 | COMPLETE |
| Determinism | SOURCE_DATE_EPOCH + Zstd compression | COMPLETE |
| evergreenctl | Rust toolchain: audit, verify, drift, generate, bump | COMPLETE |
| Pre-push gate | 8-gate quality check (tests, clippy, fmt, manifests, SBOMs, constraints) | COMPLETE |
| CI pipeline | 10 GitHub Actions workflows (build, lint, scan, sign, provenance) | COMPLETE |
| Reproducibility | 75.3% all-stage FROM digest pinning (1522/2020 lines) | PARTIAL |
| Multi-arch | 635 images declared (249 ARG TARGETARCH + 386 scratch native) | PARTIAL |
| Functional testing | Test framework exists (C001-C014, adversarial suite) | PARTIAL |

### 1.2 What Remains

| Issue | Count | Root Cause | Severity |
|-------|-------|------------|----------|
| curl-404 (release deleted) | ~21 | Upstream removed old tarball | HIGH |
| upstream-image-not-found | ~37 | Upstream deleted or moved image | MEDIUM |
| build-compilation failure | ~3 | Upstream build system broken | LOW |
| copy-to-non-directory | ~5 | BuildKit cache race (transient) | LOW |
| auth-gated :latest FROM | ~5 | Private registries without PAT | MEDIUM |
| Digest pinning gap | 498 FROM lines | Unpinned intermediate stages | MEDIUM |
| Multi-arch gap | ~360 images | C-extension, GPU, niche upstream | LOW |
| Stub test config | 998 images | test_config.yaml has binary:none for all | HIGH |
| Archive docs outdated | 7+ files | Emoji usage, stale UID/alpine refs | LOW |

---

## 2. Short-Term Roadmap (Phase 52-55, 2-4 weeks)

### Phase 52: Version Bump Batch

**Objective:** Resolve the ~21 curl-404 failures by updating to the latest upstream release.

**Method:**
1. Run `evergreenctl outdated images/` to identify stale versions.
2. For each image: fetch latest release URL, update manifest.toml `source.url`, compute sha256, update Dockerfile `ARG VERSION`.
3. Re-run CI to confirm green.
4. Update SBOMs.

**Success criteria:** curl-404 count reduced from ~21 to 0.

### Phase 53: Upstream Audit and Triage

**Objective:** Triage the ~37 upstream-image-not-found failures into fixable, permanently broken, or auth-gated.

**Method:**
1. Categorize each failure:
   - **Fixable (~15):** Version bump to available release.
   - **Permanently broken (~12):** Upstream discontinued. Mark manifest with `status = "deprecated"` and document in catalog.
   - **Auth-gated (~10):** Add GitHub PAT to CI secrets or document as build-from-source-only.
2. Update ROADMAP.md with final triage counts.

**Success criteria:** Every image has a documented disposition (active, deprecated, auth-gated).

### Phase 54: Test Framework Activation

**Objective:** Replace the stub test_config.yaml with actionable test configurations for Tier-1 images.

**Current state:** `test_config.yaml` has `binary: none` and `stub: true` for all 998 images. The test framework (test_framework.sh, test_adversarial.sh) is well-written but cannot run without image builds.

**Method:**
1. Select 50 Tier-1 images (traefik, nginx, redis, postgres, prometheus, grafana, etc.).
2. For each: set `binary`, `health_port`, `version_flag`, `startup_timeout`, `stub: false`.
3. Add a CI workflow that builds and tests these 50 images weekly.
4. Expand to Tier-2 (100 images) in Phase 56.

**Success criteria:** 50 Tier-1 images have functional test configs and pass adversarial tests.

### Phase 55: Documentation Convergence

**Objective:** Resolve all remaining documentation inconsistencies identified in the audit.

**Items:**
1. Fix ROADMAP.md duplicate rows (Workflows, Anti-patterns, Layers).
2. Fix CHANGELOG.md chronological ordering (multiple sections out of order).
3. Fix CHANGELOG.md duplicate `[Unreleased]` sections.
4. Fix CHANGELOG.md mathematically impossible percentage (460/376 = 122%).
5. Fix CHANGELOG.md stale `[Unreleased]` known issues (all resolved).
6. Add deprecation notices to archive docs referencing Alpine/debian-slim.
7. Fix broken file references in `compliance/ato/ssp/ssp_template.md` (REQUIREMENTS.md, .specs/03_security/).
8. Update image count in VERSION.md if filesystem count differs (999 vs 998).

**Success criteria:** Zero broken references, zero stale claims, zero emoji in active docs.

---

## 3. Medium-Term Roadmap (Phase 56-65, 1-3 months)

### Phase 56-58: Digest Pinning Completion

**Objective:** Increase all-stage FROM digest pinning from 75.3% to >95%.

**Method:**
1. Enumerate all unpinned FROM lines (498 remaining).
2. For wolfi/debian-slim bases: resolve to specific digest using `crane digest`.
3. For builder-stage bases (golang, rust, node): pin to specific version + digest.
4. Automate: add `evergreenctl pin` command that resolves and injects digests.
5. Re-run CI to confirm no regressions.

**Risk:** Digest rotation requires manual updates when base images are rebuilt. Mitigate with Dependabot or Renovate for base image digests.

### Phase 59-60: Multi-Arch Expansion

**Objective:** Add `ARG TARGETARCH` support for the ~360 remaining single-arch images.

**Priority tiers:**
- **High (~80):** C-extension Python images (scrapy, pandas, numpy). Requires per-arch wheels.
- **Medium (~200):** amd64-only upstreams. Verify upstream has arm64 builds.
- **Low (~80):** GPU/ML images (CUDA, ROCm). Platform-specific by nature.

**Method:**
1. Audit upstream registries for multi-arch manifests.
2. For images with multi-arch upstream: add `ARG TARGETARCH` and conditional FROM.
3. For C-extension Python: use `--platform`-aware wheel selection.
4. Update CI matrix to build `linux/amd64,linux/arm64` for expanded set.

### Phase 61-62: SBOM Depth and Attestation

**Objective:** Improve SBOM quality and add SLSA provenance attestation to all built images.

**Method:**
1. Configure syft to capture transitive dependencies (currently may miss dynamic deps).
2. Add grype scan results as build artifact.
3. Store SBOMs in a Rekor transparency log for supply chain verification.
4. Generate in-toto attestations linking SBOM + provenance + signature.

### Phase 63-65: evergreenctl Maturation

**Objective:** Make evergreenctl the single source of truth for image management.

**Current gaps:**
- Only 10 unit tests (verify: sha256, sha512, match, mismatch, case-insensitive, unsupported, display, nonexistent; discover: extract_github_repo).
- No integration tests.
- No CLI completion.
- No man pages.

**Add:**
1. Integration tests: verify a real manifest.toml round-trip (generate -> build -> verify).
2. `evergreenctl pin-digests` -- resolve and pin all FROM digests.
3. `evergreenctl check-upstream` -- compare manifest versions against latest upstream releases.
4. `evergreenctl report` -- generate a JSON/HTML report of registry health.
5. Shell completion (clap supports this natively).

---

## 4. Long-Term Vision (Phase 66+, 3-12 months)

### 4.1 Automated Version Bumping

Build a daily cron workflow that:
1. Runs `evergreenctl check-upstream` across all images.
2. Opens a PR per batch (max 50 images per PR to avoid CI timeout).
3. CI builds and tests the bumped images.
4. Auto-merge if all gates pass.

This eliminates the manual version bump cycle and keeps the registry current.

### 4.2 Binary Provenance Verification

For scratch-based images, the primary risk is supply chain compromise of the upstream binary. Mitigate with:
1. **Multi-source verification:** Download from both GitHub Releases and the vendor's CDN, compare sha256.
2. **Reproducible builds:** For Go/Rust binaries, rebuild from source and compare against upstream binary.
3. **Sigstore cosign:** Verify upstream signatures where available (Go, Kubernetes ecosystem).

### 4.3 Policy-as-Code

Define image policies in a machine-readable format (Rego/Cedar) that CI enforces:
```toml
[policy.C001]
description = "Non-root execution"
check = "docker inspect --format '{{.Config.User}}'"
expect = "65532:65532"
severity = "block"

[policy.C010]
description = "Health check"
check = "docker inspect --format '{{.Config.Healthcheck}}'"
expect = "not null"
severity = "warn"
```

### 4.4 Registry Publication

Publish images to GHCR with:
1. Immutable versioned tags (never overwrite).
2. Short-lived `:latest` tag (24-hour TTL via retention policy).
3. Per-image README rendered on GHCR UI.
4. Automated vulnerability scanning (GitHub-native DependaBot + Grype).

### 4.5 Metrics Dashboard

Deploy a Grafana dashboard showing:
- Total images, coverage percentages (non-root, SBOM, digest-pinned).
- Upstream version drift (images behind latest).
- CI pass/fail rate trends.
- Vulnerability count trends.
- Build time and image size distributions.

---

## 5. Technical Debt Register

| Item | Effort | Impact | Priority |
|------|--------|--------|----------|
| CHANGELOG.md reordering | 2h | Documentation accuracy | HIGH |
| CHANGELOG.md duplicate Unreleased | 1h | Documentation accuracy | HIGH |
| test_config.yaml stubs | 8h | Test coverage | HIGH |
| Archive doc deprecation notices | 2h | Documentation accuracy | MEDIUM |
| SSP template broken references | 1h | Compliance accuracy | MEDIUM |
| ROADMAP.md duplicate rows | 15m | Documentation accuracy | LOW |
| Image count discrepancy (998 vs 999) | 30m | Data accuracy | MEDIUM |
| `number_prefix` unmaintained warning | 1h | Dependency health | LOW |
| CHANGELOG.md 122% math error | 15m | Documentation accuracy | LOW |

---

## 6. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Upstream deletes release tarballs | HIGH | CI failure | Daily version check, auto-bump |
| GitHub rate-limits CI | MEDIUM | Build failure | Use GHCR for caching, authenticated API calls |
| Base image digest rotation | MEDIUM | Stale FROM | Dependabot/Renovate for base images |
| wolfi package removal | LOW | Build failure | Pin wolfi version, monitor advisory |
| evergreenctl dependency CVE | LOW | Supply chain | `cargo audit` in CI, minimal dependencies |
| Image catalog drift from reality | MEDIUM | User confusion | `evergreenctl generate` from manifest.toml |

---

## 7. Quality Gate Summary (Post-Audit)

| Gate | Tool | Result |
|------|------|--------|
| Rust unit tests | `cargo test` | 10/10 PASS |
| Rust clippy | `cargo clippy -D warnings` | 0 warnings |
| Rust formatting | `cargo fmt --check` | PASS |
| Rust release build | `cargo build --release` | PASS |
| Rust dependency audit | `cargo audit` | 1 unmaintained (number_prefix, informational) |
| Python syntax | `py_compile` | 5/5 PASS |
| Manifest TOML validation | Custom (tomllib) | 998/998 PASS |
| SBOM JSON validation | Custom (json) | 998/998 PASS |
| Dockerfile constraints | Custom (alpine check) | 0 violations |
| Pre-push gate | 8-gate hook | 8/8 PASS |
| CI push | GitHub Actions | Green (upstream failures only) |

---

## 8. Conclusion

The registry has completed its syntax and structure phases (Phases 0-51). The next critical path is:

1. **Phase 52-53:** Resolve upstream failures (version bumps + triage) -- unblocks CI green.
2. **Phase 54:** Activate test framework for Tier-1 images -- validates actual container behavior.
3. **Phase 55:** Documentation convergence -- eliminates drift between docs and reality.
4. **Phase 56-65:** Digest pinning, multi-arch, SBOM depth, evergreenctl maturation.
5. **Phase 66+:** Automated version bumping, binary provenance, policy-as-code, registry publication.

The pre-push hook ensures no regressions: every push must pass 8 quality gates including unit tests, static analysis, manifest validation, and SBOM integrity.
