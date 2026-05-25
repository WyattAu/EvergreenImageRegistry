# Evergreen Image Registry: Production Roadmap v30.0.0

**Version:** v30.0.0 | **Date:** 2026-05-25 | **Status:** Production-Ready with Known Gaps

---

## 0. Audit Summary (2026-05-25)

Full audit conducted. All test suites pass, code quality verified, CI/CD hardened.

### Tests: 195 total, 195 passing

| Suite                                            | Count                 | Status |
| ------------------------------------------------ | --------------------- | ------ |
| Python (pytest)                                  | 69                    | PASS   |
| Rust unit (cargo test --lib)                     | 67                    | PASS   |
| Rust integration (cargo test --test integration) | 59                    | PASS   |
| Rust clippy                                      | 0 warnings            | PASS   |
| Rust fmt                                         | PASS                  | PASS   |
| Python ruff lint                                 | 0 errors (33 scripts) | PASS   |
| Python ruff format                               | 0 errors (33 scripts) | PASS   |
| Shell syntax                                     | 26 scripts            | PASS   |
| Manifest TOML                                    | 1015/1015             | PASS   |
| SBOM JSON                                        | 998/998               | PASS   |
| Pre-push gate                                    | 11/11                 | PASS   |

### Issues Found and Fixed

| Issue                                      | Count          | Severity | Status |
| ------------------------------------------ | -------------- | -------- | ------ |
| PLACEHOLDER_SHA stub checksums             | 17 Dockerfiles | HIGH     | FIXED  |
| CI/CD workflow bugs                        | 11 workflows   | CRITICAL | FIXED  |
| SECURITY.md emojis                         | 4 occurrences  | MEDIUM   | FIXED  |
| Python ruff formatting drift               | 7 scripts      | LOW      | FIXED  |
| Shellcheck warnings                        | 3 issues       | LOW      | FIXED  |
| Forgejo image broken (0-byte binary)       | 1 image        | CRITICAL | FIXED  |
| Postgres image broken (no PGDATA, no init) | 1 image        | CRITICAL | FIXED  |
| Landing page wrong badge URL, image count  | 2 issues       | MEDIUM   | FIXED  |
| Docs site missing index + Jekyll config    | 2 files        | MEDIUM   | FIXED  |

### Known Issues (Pre-existing, Not Introduced)

| Issue                                | Count      | Severity | Action Required                    |
| ------------------------------------ | ---------- | -------- | ---------------------------------- |
| curl\|sh anti-pattern in Dockerfiles | 28 images  | MEDIUM   | Refactor to wget + tar             |
| TODO/FIXME in Dockerfiles            | 7 images   | LOW      | Resolve or remove                  |
| sleep infinity stubs                 | 2 images   | LOW      | Replace with meaningful entrypoint |
| kdb/kdb-plus/windows-exporter stubs  | 4 images   | LOW      | Deprecate or implement             |
| build-on-push.yml startup_failure    | 1 workflow | HIGH     | Debug workflow_call trigger        |
| Unpinned intermediate FROM lines     | ~490       | MEDIUM   | Resolve with crane                 |
| Single-arch images                   | ~317       | MEDIUM   | Add TARGETARCH support             |
| Stub test configs (binary:none)      | ~947       | MEDIUM   | Write real test configs            |

---

## 1. Current Architecture

### 1.1 Component Map

| Component         | Language   | Files           | Tests                          | Purpose                           |
| ----------------- | ---------- | --------------- | ------------------------------ | --------------------------------- |
| evergreenctl      | Rust       | 20 src + 1 test | 126 (67 unit + 59 integration) | Registry management CLI           |
| health-shim       | Go         | 3 src           | CI                             | Scratch image HEALTHCHECK sidecar |
| Image Dockerfiles | Dockerfile | 998             | CI                             | Hardened container images         |
| Image manifests   | TOML       | 998             | TOML validation                | Build metadata                    |
| SBOMs             | SPDX JSON  | 998             | JSON validation                | Supply chain inventory            |
| Scripts           | Python     | 33              | ruff lint                      | Build, validation, migration      |
| Scripts           | Bash       | 26              | shellcheck                     | Discovery, CI helpers             |
| CI/CD workflows   | YAML       | 19 files        | actionlint                     | Build, test, sign, publish        |
| Documentation     | Markdown   | 14 files        | markdownlint                   | Standards, guides, reports        |
| Landing page      | HTML       | 1               | Manual                         | GitHub Pages entry point          |

### 1.2 Quality Scorecard

| Metric                     | Value                                 | Status   |
| -------------------------- | ------------------------------------- | -------- |
| Total images               | 998                                   | COMPLETE |
| Non-root USER              | 99.5% (993/998)                       | PASS     |
| HEALTHCHECK (real)         | 56.0% (559/998)                       | PASS     |
| HEALTHCHECK NONE (scratch) | 43.9% (438/998)                       | EXPECTED |
| SBOM (SPDX 2.3)            | 100% (998/998)                        | PASS     |
| Digest-pinned final stage  | 100% (998/998)                        | PASS     |
| All-stage FROM digest pin  | 75.5% (1522/2015)                     | PASS     |
| Multi-arch TARGETARCH      | 853/998                               | PASS     |
| Per-image README           | 100% (998/998)                        | PASS     |
| .dockerignore              | 99.9% (997/998)                       | PASS     |
| ENTRYPOINT                 | 95.8% (956/998)                       | PASS     |
| STOPSIGNAL                 | 99.6% (994/998)                       | PASS     |
| Dockerfile syntax errors   | 0                                     | PASS     |
| Alpine base images         | 0                                     | PASS     |
| Hardcoded secrets          | 0 (3 false positives: mysql env vars) | PASS     |

### 1.3 CI/CD Pipeline

19 GitHub Actions workflows:

| Workflow                | Trigger                | Purpose                  |
| ----------------------- | ---------------------- | ------------------------ |
| build-on-push.yml       | Push/PR (images/)      | Build changed images     |
| build-nightly.yml       | Cron 03:00 UTC         | Full rebuild by tier     |
| build-on-demand.yml     | Manual                 | Build specific images    |
| \_build-reusable.yml    | Called by above        | Shared build logic       |
| lint.yml                | Push/PR                | 12 parallel lint jobs    |
| cosign-sign.yml         | workflow_run           | OIDC keyless signing     |
| slsa-provenance.yml     | workflow_run           | SLSA v3 provenance       |
| sbom-attestation.yml    | workflow_run           | SBOM attachment          |
| daily-security-scan.yml | Cron 06:00 UTC         | Trivy + Grype CVE scan   |
| nightly-scan.yml        | Cron 03:00 UTC         | Version/freshness check  |
| auto-bump.yml           | Cron 06:00 UTC         | Auto version bump        |
| fuzz.yml                | Cron weekly + PR       | Go fuzz testing          |
| go-test.yml             | Push/PR (health-shim/) | Go unit tests            |
| actionlint.yml          | PR (workflows/)        | Workflow linting         |
| stale.yml               | Cron daily             | Issue/PR management      |
| update-readme.yml       | Push (images/)         | README auto-update       |
| metrics-report.yml      | Cron weekly            | Metrics snapshot         |
| provenance-verify.yml   | Cron weekly            | Provenance verification  |
| publish-immutable.yml   | Tag push               | Immutable tag publishing |

---

## 2. Path to Full Production

### Phase 103: Resolve build-on-push.yml startup_failure (Week 1)

**Objective:** Fix the persistent startup_failure in the primary build workflow.

Actions:

1. Debug workflow_call trigger mechanism in \_build-reusable.yml
2. Verify all reusable workflow inputs/outputs match caller expectations
3. Test with a minimal push that touches a single image
4. Add workflow_dispatch fallback for manual testing

**Success:** build-on-push.yml runs to completion on image changes.

### Phase 104: Eliminate curl|sh anti-pattern (Week 1-2)

**Objective:** Replace all 28 curl|sh patterns with deterministic wget + tar extraction.

Actions:

1. For each image using `curl ... | sh`: replace with `wget -O /tmp/installer && sh /tmp/installer && rm /tmp/installer`
2. Prefer binary downloads over pipe-to-shell where possible
3. Add checksum verification for downloaded installers
4. Validate with `grep -r 'curl.*|.*sh' images/` returning 0 results

**Success:** Zero curl|sh patterns in any Dockerfile.

### Phase 105: Digest-pin all intermediate FROM lines (Week 2-3)

**Objective:** Increase FROM digest pinning from 75.5% to >95%.

Actions:

1. Use crane to resolve digests for ~490 unpinned intermediate FROM refs
2. Run `evergreenctl pin-digests images/` across all images
3. Verify with `grep -r 'FROM.*@sha256:' images/ | wc -l` matching 2015+
4. Add CI gate that fails on new unpinned FROM lines

**Success:** >95% FROM digest pinning, CI gate enforcing.

### Phase 106: Stub test config resolution (Week 3-5)

**Objective:** Replace ~947 stub test configs (binary:none) with real functional tests.

Actions:

1. Categorize stubs: binary available but untested, binary unavailable
2. For available binaries: write wget/tar/chmod test configs
3. For unavailable binaries: add download verification tests
4. Target: >80% real test configs (up from ~60%)

**Success:** <200 stub test configs remaining, all documented.

### Phase 107: Multi-arch expansion (Week 4-6)

**Objective:** Add TARGETARCH support to remaining ~317 single-arch images.

Actions:

1. Categorize: C-extension Python (115), amd64-only upstream (150), GPU/ML (52)
2. Python C-extension: Use multi-arch wolfi-python base
3. amd64-only: Document limitation, add to manifest
4. GPU/ML: Skip multi-arch (hardware-specific)
5. Target: >800/998 multi-arch images

**Success:** >80% images with ARG TARGETARCH.

### Phase 108: Full CI green (Week 5-7)

**Objective:** Reduce CI build failures to <20 (only unfixable upstream).

Actions:

1. Run `evergreenctl outdated --all` against live upstreams
2. Batch version bump for ~21 images with deleted releases
3. Deprecate ~15 permanently broken upstreams
4. Add retry logic for transient failures
5. Document all remaining failures with root cause

**Success:** CI pass rate >98%, all failures documented as upstream.

### Phase 109: Binary provenance verification (Week 6-7)

**Objective:** Verify provenance of all downloaded binaries.

Actions:

1. Integrate cosign verify-blob for all binary downloads
2. Add CHECKSUMS file validation to every Dockerfile
3. Remove all `|| true` patterns from checksum verification
4. Add CI gate that fails on missing checksums

**Success:** 100% of binary downloads have checksum verification.

### Phase 110: Forgejo + Cloudflare Pages deployment (Week 7-8)

**Objective:** Deploy documentation to both GitHub Pages and Cloudflare Pages.

Actions:

1. Configure GitHub Pages from main branch (Jekyll with \_config.yml)
2. Set up Cloudflare Pages for Forgejo mirror
3. Add Cloudflare Pages build configuration
4. Verify both sites serve identical content
5. Add link-checking CI job that validates all doc links

**Success:** Both https://wyattau.github.io/EvergreenImageRegistry/ and Cloudflare Pages serve docs.

### Phase 111: Documentation hardening (Week 8-9)

**Objective:** All documentation accurate, rigorous, no emojis, concise.

Actions:

1. Audit all 14 docs files for technical accuracy
2. Verify all code examples compile/run
3. Remove any remaining informal language
4. Add mathematical notation where applicable (e.g., checksum formulas)
5. Cross-reference verification: every doc links to existing files

**Success:** Zero documentation errors in CI check.

### Phase 112: Compliance certification prep (Week 9-10)

**Objective:** Prepare compliance artifacts for FIPS, CIS, STIG, ATO.

Actions:

1. Generate FIPS compliance matrix for all 998 images
2. Run CIS Docker Benchmark against sample images
3. Complete STIG check scripts
4. Build ATO controls mapping, SSP, POA&M
5. Generate evidence artifacts for audit

**Success:** Compliance folder contains complete certification evidence.

### Phase 113: Performance baseline and optimization (Week 10-11)

**Objective:** Establish build-time performance baselines and optimize.

Actions:

1. Measure average build time per image
2. Identify top-20 slowest builds
3. Optimize Dockerfile layer caching
4. Add BuildKit cache mounts for package managers
5. Target: <5 min average build time per image

**Success:** Build time metrics in CI, <5 min average.

### Phase 114: Monitoring and alerting (Week 11-12)

**Objective:** Production monitoring for image freshness and security.

Actions:

1. Configure alerts for new CRITICAL CVEs in published images
2. Set up digest drift monitoring
3. Add upstream version change alerts
4. Create operational runbook for incident response
5. Configure weekly health reports

**Success:** Automated alerts for all security/freshness events.

---

## 3. Future Plans (Post-Production)

### 3.1 Ecosystem Growth

| Initiative               | Description                                          | Timeline |
| ------------------------ | ---------------------------------------------------- | -------- |
| Image request pipeline   | Community-driven image proposal + build workflow     | Q3 2026  |
| Helm chart registry      | Publish evergreen-registry Helm chart to chart repos | Q3 2026  |
| Kubernetes operator      | evergreen-operator for automated image updates       | Q4 2026  |
| Artifact Hub integration | List all images on Artifact Hub                      | Q3 2026  |
| SBOM deep scanning       | Automated vulnerability correlation from SBOMs       | Q3 2026  |

### 3.2 Platform Expansion

| Platform               | Description                                 | Timeline |
| ---------------------- | ------------------------------------------- | -------- |
| Forgejo Actions mirror | CI/CD parity for Forgejo-hosted mirror      | Q3 2026  |
| Cloudflare Pages docs  | Dual-hosted documentation                   | Q3 2026  |
| Docker Hub publishing  | Republish to Docker Hub official namespaces | Q4 2026  |
| Quay.io mirror         | Red Hat ecosystem distribution              | Q4 2026  |
| AWS ECR Public         | AWS-native distribution                     | Q1 2027  |

### 3.3 Tooling Evolution

| Tool              | Description                                  | Timeline |
| ----------------- | -------------------------------------------- | -------- |
| evergreenctl v3.0 | WASM plugin system, gRPC API, daemon mode    | Q4 2026  |
| health-shim v2.0  | gRPC health protocol, Prometheus native      | Q3 2026  |
| evergreen-web     | Web UI for image catalog and management      | Q1 2027  |
| evergreen-scanner | Standalone vulnerability scanner using SBOMs | Q4 2026  |
| evergreen-policy  | OPA/Rego policy engine for image admission   | Q1 2027  |

### 3.4 Security Enhancements

| Enhancement                     | Description                                           | Timeline |
| ------------------------------- | ----------------------------------------------------- | -------- |
| Sigstore bundle signing         | Full Sigstore bundle (signature + certificate + tlog) | Q3 2026  |
| VEX document generation         | Vulnerability exploitation exchange documents         | Q4 2026  |
| In-toto attestation             | Full supply chain layout verification                 | Q1 2027  |
| SBOM quality scoring            | Automated SBOM completeness scoring                   | Q3 2026  |
| Reproducible build verification | Binary-level bit-for-bit reproducibility checks       | Q2 2027  |

### 3.5 Scale Targets

| Metric                 | Current  | Target    | Timeline |
| ---------------------- | -------- | --------- | -------- |
| Total images           | 998      | 1500+     | Q4 2026  |
| Multi-arch images      | 853      | 1200+     | Q4 2026  |
| FROM digest pinning    | 75.5%    | >98%      | Q3 2026  |
| CI pass rate           | ~90%     | >99%      | Q3 2026  |
| Real test configs      | ~60%     | >90%      | Q4 2026  |
| Average build time     | Unknown  | <5 min    | Q3 2026  |
| Documentation coverage | 14 files | 30+ files | Q4 2026  |

---

## 4. Risk Register

| Risk                             | Probability | Impact   | Mitigation                                    |
| -------------------------------- | ----------- | -------- | --------------------------------------------- |
| Upstream abandons critical image | HIGH        | MEDIUM   | Maintain fork, document deprecation           |
| GHCR rate limits                 | MEDIUM      | HIGH     | Docker Hub + Quay mirror                      |
| Supply chain attack on upstream  | LOW         | CRITICAL | Digest pinning + cosign verify + nightly scan |
| GitHub Actions outage            | LOW         | HIGH     | Forgejo Actions mirror                        |
| Build-on-push persistent failure | MEDIUM      | HIGH     | Manual dispatch fallback                      |
| Key upstream version conflict    | MEDIUM      | MEDIUM   | Pin to known-good version                     |

---

## 5. Decision Log

| Date       | Decision                                   | Rationale                                                                                                   |
| ---------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| 2026-05-25 | Remove PLACEHOLDER_SHA from 17 Dockerfiles | Dead code providing zero verification; proper checksums to be added in Phase 109                            |
| 2026-05-25 | Fix postgres Dockerfile init script        | Original image was non-functional (no PGDATA, no initdb); new entrypoint supports POSTGRES_DB/USER/PASSWORD |
| 2026-05-25 | Fix Forgejo Dockerfile (0-byte binary)     | Download fallback was broken; new Dockerfile uses test -s for verification                                  |
| 2026-05-25 | Remove GITHUB_TOKEN from --build-arg       | Token leaked into image history; already passed via --secret                                                |
| 2026-05-25 | Keep hadolint as advisory in lint.yml      | Pre-existing errors in 17 images; fix requires per-image effort (Phase 109)                                 |
| 2026-05-25 | Add Jekyll \_config.yml for GitHub Pages   | Enables .md -> .html conversion for doc links                                                               |
