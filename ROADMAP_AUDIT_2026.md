# Evergreen Image Registry -- Roadmap to Production

## Current State (May 2026)

- 987 active image directories (1015 Dockerfiles total)
- 974 real images, 11 placeholders, 1 stub, 0 errors
- 114 Rust tests (67 unit + 47 integration) passing
- 13/13 CI lint jobs passing
- GitHub Pages configured (landing page deployed)
- evergreenctl v1.0.0 with 19 subcommands
- SLSA provenance, Cosign signing, SBOM generation workflows in place
- Tier-aware build pipeline (critical/standard/community/experimental)

## Audit Results Summary

### Code Quality (evergreenctl -- Rust)
- 38 issues found (3 CRITICAL, 12 HIGH, 14 MEDIUM, 9 LOW)
- All 3 CRITICAL and key HIGH issues fixed in this audit cycle
- Remaining: centralize regex compilation (LazyLock), inject time for testability, centralize user agent string

### Code Quality (scripts -- Python)
- 33 issues found (3 CRITICAL, 13 HIGH, 11 MEDIUM, 6 LOW)
- All 3 CRITICAL and key HIGH issues fixed in this audit cycle
- Remaining: migrate print() to logging, add type hints to 80+ functions, fix module-level mutable state

### CI/CD (20 workflows)
- 5 CRITICAL, 12 HIGH, 18 MEDIUM, 11 LOW findings
- Key issues: actions pinned to mutable tags, GITHUB_TOKEN passed as build-arg, broken sbom-attestation workflow, 1200+ matrix jobs in deprecated build.yml

### Documentation (26+ files)
- 4 CRITICAL, 11 HIGH, 10 MEDIUM, 6 LOW findings
- Key fix: wolfi libc claim corrected (glibc, not musl)
- Remaining: reconcile image counts across all docs, fix registry URLs in 8 image READMEs, reorder CHANGELOG

---

## Phase 1: Hardening (Weeks 1-2)

### P0 -- Security (blocks production)
1. Pin all GitHub Actions to commit SHA (not mutable tags)
   - 20 workflows x ~5 actions each = ~100 pin operations
   - Use `pinact` or `actions/attest-build-provenance` for automation
2. Replace GITHUB_TOKEN build-arg with BuildKit secret mounts
   - Affects: _build-reusable.yml, build.yml, build-on-push.yml
3. Fix sbom-attestation.yml (broken workflow_run trigger, impossible if condition)
4. Remove secrets:inherit from reusable workflow callers, pass explicitly
5. Fix publish-immutable.yml (malformed API URL, missing needs dependency)

### P1 -- Test Coverage
1. Add Go tests for health-shim (currently only vet+build in CI)
2. Add property-based tests (proptest/QuickCheck) for evergreenctl verify module
3. Add shellcheck SC errors enforcement (currently advisory)
4. Target: 95% branch coverage on evergreenctl critical paths

### P2 -- Version Reconciliation
1. Fix 84 version mismatches between Dockerfile and manifest.toml
2. Automate sync via evergreenctl drift detection in CI
3. Regenerate all image READMEs from manifest.toml data

---

## Phase 2: Infrastructure (Weeks 3-4)

### P0 -- Pipeline Consolidation
1. Archive deprecated workflows (build.yml, build-and-push.yml)
2. Update daily-security-scan.yml to dispatch to build-on-demand.yml
3. Remove 1200-job build-multiarch matrix (replace with dynamic discovery)
4. Add CODEOWNERS for .github/workflows/

### P1 -- Observability
1. Deploy Grafana dashboard from docs/metrics-dashboard.md
2. Wire Prometheus metrics from build pipeline
3. Add alerting on: CRITICAL CVEs, build failures >24h, digest pin drift

### P2 -- Documentation Site
1. Deploy docs site via GitHub Pages (Jekyll or static generator)
2. Convert docs/*.md to proper HTML with navigation
3. Add search functionality (Algolia DocSearch or similar)
4. Fix all broken relative links in documentation

---

## Phase 3: Production Readiness (Weeks 5-8)

### P0 -- Supply Chain
1. Implement GITHUB_TOKEN secret mounting in all Dockerfiles
2. Achieve 100% digest pinning on all FROM lines (currently ~74%)
3. Automate SBOM attestation via fixed sbom-attestation workflow
4. Enable keyless Cosign signing with Sigstore OIDC federation

### P1 -- evergreenctl Improvements
1. Centralize all Regex::new() into LazyLock statics (23 call sites)
2. Centralize user agent string via env!("CARGO_PKG_VERSION") (4 locations)
3. Inject time dependencies for deterministic testing (4 modules)
4. Add --registry flag to sign command
5. Add --limit flag to changelog command
6. Replace hardcoded "images" path in bump.rs with configurable parameter

### P2 -- Python Script Improvements
1. Migrate all 31 scripts from print() to logging module
2. Add type hints to 80+ public functions across 22 files
3. Move module-level logic into main() functions (3 scripts)
4. Replace bare except Exception with specific exception types (6 scripts)

### P3 -- Compliance
1. Update all document image counts to verified numbers
2. Fix CHANGELOG.md version ordering (reverse chronological)
3. Reconcile all metric inconsistencies across README, ROADMAP, VERSION
4. Run full compliance matrix audit against IEC 62443, NIST SP 800-53

---

## Phase 4: Scale and Automation (Weeks 9-12)

### P0 -- Build Performance
1. Implement dynamic build matrix (discover at runtime, not hardcoded)
2. Add build caching strategy (layer cache across runs)
3. Parallelize image builds across multiple runners
4. Target: <2 hour full rebuild time

### P1 -- Automated Version Management
1. Implement auto-bump from upstream release monitoring
2. Add version constraint validation (semver range checking)
3. Automated PR generation for version updates with diff preview
4. Rate limit auto-rebuilds (max 1/day per CVE severity tier)

### P2 -- Multi-Architecture
1. Verify arm64 builds for all critical-tier images
2. Add QEMU emulation tests for C/C++/Rust cross-compilation images
3. Implement architecture-specific test suites
4. Target: 100% multi-arch for critical tier, 80% for standard

---

## Phase 5: Ecosystem (Weeks 13-16)

### P1 -- API and Integrations
1. Build registry API (image metadata, vulnerability status, version history)
2. Add Terraform provider for image provisioning
3. Add Kubernetes operator for automated image updates
4. Build Slack/Discord webhook for build failure notifications

### P2 -- Community
1. Publish contributing guidelines (already in docs/)
2. Add issue templates for image requests, bug reports
3. Implement automated image proposal workflow
4. Add sponsor/funding infrastructure

---

## Phase 6: Advanced (Quarter 3-4 2026)

### Supply Chain Security
1. Implement SLSA Level 3 provenance for all builds
2. Add in-toto attestations for build pipeline integrity
3. Implement VEX (Vulnerability Exploitability Exchange) documents
4. Automate CVE response with VEX-driven suppress/patch decisions

### Performance
1. Implement OCI image distribution via Zot registry
2. Add image layer deduplication analysis
3. Implement progressive image delivery (zstd:chunked)
4. Target: average image size reduction of 20%

### AI/ML Pipeline Integration
1. Build GPU variant images with deterministic CUDA pinning
2. Add model-serving base images (vLLM, TensorRT, ONNX Runtime)
3. Implement MLOps pipeline integration (MLflow, Weights & Biases)
4. Target: 50+ ML-serving images in critical/standard tiers

---

## Metrics and Success Criteria

| Metric | Current | Target (Phase 3) | Target (Phase 6) |
|--------|---------|-------------------|-------------------|
| Active images | 987 | 1000+ | 1200+ |
| Test pass rate | 100% (114/114) | 100% (200+) | 100% (400+) |
| Digest pinning | 74% | 95% | 100% |
| SBOM coverage | 998/987 | 100% | 100% |
| CRITICAL CVEs (unresolved) | Unknown | 0 | 0 |
| Build time (full) | ~6 hours | <4 hours | <2 hours |
| Multi-arch (critical) | ~60% | 90% | 100% |
| Doc accuracy | ~80% | 95% | 99% |
| CI lint pass | 13/13 | 13/13 | 15/15 |

---

## Known Risks

1. **GitHub Actions minute consumption**: Full rebuild of 1000+ images costs ~3000 minutes/night. Mitigation: tier-prioritized builds, caching.
2. **Upstream breaking changes**: Wolfi base image updates may break Dockerfiles. Mitigation: nightly canary builds, automated rollback.
3. **Supply chain attacks**: Mutable action tags are the primary vector. Mitigation: SHA pinning (Phase 1 P0).
4. **Rate limiting**: GitHub API rate limits (60/hour unauthenticated) for version checking. Mitigation: authenticated requests, caching.
5. **Image bloat**: Some images exceed 200MB limit. Mitigation: size enforcement in CI, scratch/distroless migration.

---

## Appendix: Pre-existing CI/CD Failures (Not Caused by This Audit)

The following workflows fail on every push (pre-existing, infrastructure issues):
- `.github/workflows/slsa-provenance.yml` -- Invalid workflow structure
- `.github/workflows/auto-bump.yml` -- Invalid workflow structure
- `.github/workflows/provenance-verify.yml` -- Invalid workflow structure
- `.github/workflows/sbom-attestation.yml` -- Invalid workflow_run trigger
- `Build on Push` -- Git authentication failure during checkout (needs token configuration)

These should be fixed as part of Phase 2 P0 (Pipeline Consolidation).
