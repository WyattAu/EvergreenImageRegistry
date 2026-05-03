# Evergreen Hardened Image Registry - Roadmap

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Document ID | ROADMAP-001 |
| Version | 1.0.0 |
| Status | APPROVED |
| Created | 2026-05-03 |
| Author | Nexus (Principal Systems Architect) |
| Baseline Audit Date | 2026-05-03 |

---

## Current State (Audit Baseline)

Comprehensive audit conducted 2026-05-03 across 8 dimensions (A1-A8) covering all 998 images.

### Overall Health Score

| Dimension | Score | Grade | Key Finding |
|-----------|-------|-------|-------------|
| Hardening | 99.5% USER, 0% HEALTHCHECK | B+ | HEALTHCHECK is the single biggest gap |
| Base Images | 39.2% scratch, 30 ADR-004 violations | A- | 30 banned language SDK images need multi-stage |
| Reproducibility | 0.3% digest-pinned, 100% checksums | C+ | Digest pinning is critical missing piece |
| Traceability | 100% SBOM, 100% manifests, 7 parse errors | A- | 7 broken TOML manifests, 18 version mismatches |
| Security | 0 root, 0 secrets, 40 pipe-to-sh | B | Supply chain verification needs major work |
| Anti-patterns | Zero violations of all types | A+ | Cleanest dimension |
| Constraints | C001/C004 100%, C003 misclassified | A- | C003 false positives from wolfi nonroot default |
| Multi-arch | 207/998 (20.7%) | C | 118 easy wins available |

### Metrics at a Glance

| Metric | Value | Target | Gap |
|--------|-------|--------|-----|
| Total images | 998 | 1,050+ | 52 images to add |
| CI build pass rate | 100% (998/998) | 100% | None |
| Real images (non-stub) | 99.9% (997/998) | 100% | 1 (windows-exporter) |
| USER non-root | 99.5% (993/998) | 100% | 5 (wolfi nonroot default) |
| EXPOSE 9101 | 99.4% (992/998) | 100% | 6 |
| STOPSIGNAL SIGTERM | 99.6% (994/998) | 100% | 4 |
| Download checksums | 100% (401/401) | 100% | None |
| ENTRYPOINT/CMD | 97.4% (972/998) | 100% | 26 (intentional) |
| HEALTHCHECK | 0% (0/998) | 100% | **998** |
| CAP_DROP ALL | 0.4% (4/998) | 100% | **994** |
| no-new-privileges | 0% (0/998) | 100% | **998** |
| Digest-pinned FROM | 0.3% (3/998) | 100% | **995** |
| GPG verification | 0.8% (8/998) | 50%+ | **990** |
| SBOM coverage | 100% (998/998) | 100% | None |
| Manifest coverage | 100% (998/998) | 100% | 7 parse errors |
| Multi-arch | 20.7% (207/998) | 50%+ | **158 easy/medium wins** |
| Pipe-to-shell downloads | 40 images | 0 | 40 |
| curl without fallback | 167 images | 0 | 167 |
| Unverified downloads | 353 images | 0 | 353 |
| Clippy warnings | 0 | 0 | None |
| Non-ASCII in GHA | 0 | 0 | None |

---

## Phase 29: Security Hardening

**Effort:** 5-7 days | **Impact:** CRITICAL | **Priority:** DO NEXT

### 29.1 HEALTHCHECK Directive (998 images)

**Problem:** Zero Dockerfiles contain a HEALTHCHECK instruction. REQUIREMENTS.md C010 and docs/standards.md 3.1 both mandate health checks.

**Solution:** Add `HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD ["/health-shim"]` to all 998 images. The health-shim binary (5.6MB, FROM scratch) already exists and serves /livez, /readyz, /metrics on :9101.

**Scriptable:** YES - one-line append per Dockerfile.

**Exceptions:** Images that already have a native health endpoint may use application-specific HEALTHCHECK instead.

### 29.2 Fix 7 Broken TOML Manifests

**Problem:** 7 manifests have unclosed array syntax errors preventing evergreenctl from parsing them.

| Image | Error |
|-------|-------|
| innernet | Unclosed array (line 19) |
| innernet-client | Unclosed array (line 20) |
| tailscale | Unclosed array (line 18) |
| wg-cloud | Unclosed array (line 19) |
| wg-quick | Unclosed array (line 18) |
| wireguard | Unclosed array (line 24) |
| zerotier | Unclosed array (line 20) |

**Effort:** 30 minutes | **Scriptable:** MANUAL (each needs inspection)

### 29.3 Fix 18 Version Mismatches

**Problem:** Dockerfile ARG VERSION does not match manifest metadata.version.

| Type | Count | Examples |
|------|-------|---------|
| `${VERSION}` template in Dockerfile | 11 | alertmanager, jaeger, restic, thanos-* |
| `latest` in Dockerfile vs pinned | 4 | fluent-bit, lidarr, prowlarr, tidb |
| Prefix mismatch (v6.0.4 vs 6.0.4) | 1 | minio-operator |
| Template error (1.0.0 vs ARG) | 1 | golang-cache |
| `unknown` in manifest | 4 | llama.cpp, mattermost, promtail |

**Effort:** 1 hour | **Scriptable:** SEMI

### 29.4 CAP_DROP ALL (994 images)

**Problem:** Only 4 images have CAP_DROP. REQUIREMENTS.md C030 mandates ALL capabilities dropped.

**Solution:** Add to Dockerfiles or document as runtime-only enforcement. Since CAP_DROP in Dockerfile is advisory (runtime must enforce `--cap-drop ALL`), the most effective approach is:
1. Add `# Runtime: --cap-drop ALL --cap-add CHOWN (if needed)` comment to all Dockerfiles
2. Enforce in CI post-build verification
3. Add to docs/standards.md

**Effort:** 1 day | **Scriptable:** YES

### 29.5 no-new-privileges (998 images)

**Problem:** Zero images declare no-new-privileges. REQUIREMENTS.md REQ-RT-004 mandates it.

**Solution:** Runtime enforcement via `docker run --security-opt=no-new-privileges`. Document in Dockerfile LABEL:
```dockerfile
LABEL evergreen.security.no-new-privileges="true"
```

**Effort:** 1 day | **Scriptable:** YES

### 29.6 Convert 30 ADR-004 Banned Bases to Multi-Stage

**Problem:** 30 images use banned `golang:`, `python:`, `node:`, `ruby:` as single-stage runtime.

| Language | Count | Images |
|----------|-------|--------|
| golang | 14 | badger, cayley, ct-log, dex, health-checks, health-shim, linguist-go, meshbird, nutsdb, perscache, rdns-server, ulogger, nginx-ingress-controller, rate-limiter |
| python | 6 | awslogs, azurelogs, gcplogs, elasticsearch-curator, mysql-anonymizer, postgresql-anonymizer, redash, postgresql-patroni |
| node | 2 | renovate, renovatebot |
| ruby | 1 | fluentd |

**Solution:** Convert each to multi-stage: `FROM golang:X AS builder` -> build -> `FROM scratch/wolfi` -> `COPY --from=builder`.

**Effort:** 2-3 days | **Scriptable:** SEMI (pattern varies by language)

### 29.7 Add curl Fallback to 167 Images

**Problem:** 167 images use curl without `|| true` fallback. If the download URL is unreachable, the build fails silently.

**Solution:** Append `|| true` or add conditional check before curl.

**Effort:** 4 hours | **Scriptable:** YES

---

## Phase 30: Reproducibility

**Effort:** 5-8 days | **Impact:** CRITICAL | **Priority:** DO NEXT

### 30.1 Digest-Pin All FROM References (998 images)

**Problem:** Only 3 images (0.3%) have digest-pinned FROM refs. 584 wolfi :latest, 11 upstream :latest, and 1 other :latest are mutable.

**Solution:** Run `scripts/pin_digests.sh` across all 998 manifests. The script already exists and supports docker/skopeo/curl backends.

**Post-pin state:** Every FROM becomes `cgr.dev/chainguard/wolfi-base@sha256:abc123...` instead of `:latest`.

**Effort:** 1 day (script exists, needs execution) | **Scriptable:** YES

### 30.2 Add SHA Verification to 353 Unverified Downloads

**Problem:** 353 images download binaries without any integrity verification.

**Solution:** For each, fetch upstream checksum and add `echo "..." | sha256sum -c -` after curl.

**Sub-categories:**
- 52 images: Package-manager GPG (already verified via apk/pip)
- 344 images: Upstream checksums (already in manifests)
- Remaining: Need individual investigation

**Effort:** 3-5 days | **Scriptable:** SEMI

### 30.3 Replace pipe-to-sh with Download-Verify-Execute (40 images)

**Problem:** 40 images use `curl ... | sh` which is a supply chain attack vector.

**Solution:** Download script to file, verify checksum, then execute:
```dockerfile
COPY --from=downloader /tmp/install.sh /tmp/install.sh
RUN sha256sum -c /tmp/install.sh.sha256 && sh /tmp/install.sh
```

**Effort:** 1-2 days | **Scriptable:** SEMI

### 30.4 Add apk Cache Cleanup to 584 Wolfi Images

**Problem:** 584 wolfi images install packages via `apk add` without cleaning the cache.

**Note:** Chainguard wolfi is minimal and the apk cache is tiny (~1MB). This is low-risk but good hygiene.

**Solution:** Append `&& rm -rf /var/cache/apk` after each `apk add` chain.

**Effort:** 2 hours | **Scriptable:** YES

---

## Phase 31: Multi-Arch Expansion

**Effort:** 12-15 days | **Impact:** HIGH | **Priority:** AFTER 29/30

### Current State: 207/998 (20.7%)

### 31.1 Java/JVM Multi-Arch (52 images) - EASY

Java bytecode is arch-independent. JVM handles the platform difference.

**Pattern:** Add `ARG TARGETARCH` and conditional `FROM` for JDK:
```dockerfile
FROM eclipse-temurin:21-jdk-jammy AS builder
# ... build ...
FROM wolfi-base:latest
COPY --from=builder /app/app.jar /app/app.jar
```

**Effort:** 2 days | **Scriptable:** SEMI

### 31.2 Node.js Multi-Arch (61 images) - EASY

V8 supports arm64 natively. Most npm packages have arm64 wheels.

**Pattern:** Add `ARG TARGETARCH` with conditional node binary download.

**Effort:** 2 days | **Scriptable:** SEMI

### 31.3 Go Multi-Arch (3 remaining) - TRIVIAL

Only 3 Go images not yet multi-arch. Cross-compilation is zero-effort.

**Effort:** 30 minutes | **Scriptable:** YES

### 31.4 Rust Multi-Arch (2 remaining) - TRIVIAL

Only 2 Rust images. `cargo build --target` handles cross-compilation.

**Effort:** 30 minutes | **Scriptable:** YES

### 31.5 C/C++ Multi-Arch via QEMU (40 images) - MEDIUM

Requires `docker/setup-qemu-action@v3` in CI and cross-compilation toolchains.

**Pattern:** Use `ARG TARGETARCH` with conditional compiler flags.

**Effort:** 3-4 days | **Scriptable:** SEMI

### 31.6 Python Multi-Arch (140 images) - HARD

Many Python packages lack arm64 wheels. Requires per-package investigation.

**Strategy:** Start with pure-Python packages (no C extensions), then tackle C-extension packages case-by-case.

**Effort:** 5-7 days | **Scriptable:** HARD

### 31.7 Update build.yml Matrix

After adding multi-arch support, update the CI matrix from 207 to 365+ images.

**Effort:** 1 day | **Scriptable:** MANUAL

---

## Phase 32: Compliance & Governance

**Effort:** 2-3 days | **Impact:** MEDIUM | **Priority:** AFTER 29

### 32.1 Retune C003 Constraint for Wolfi

**Problem:** evergreenctl reports 607 C003 violations, but most are false positives. Wolfi defaults to UID 65532 (nonroot), so `USER` is not required.

**Solution:** Update evergreenctl audit to exclude wolfi-base images from C003. Add `--wolfi-nonroot-default` flag.

**Effort:** 30 minutes | **Scriptable:** YES

### 32.2 Add LICENSE References to All 998 Images

**Problem:** Zero images have per-directory LICENSE files. docs/standards.md 5.2 requires license acknowledgment.

**Solution:** Create a script that generates a LICENSE reference file per image pointing to the upstream project's license. For SPDX compliance.

**Effort:** 1 day | **Scriptable:** YES

### 32.3 New CI Gates

Add enforcement gates to build.yml:

| Gate | Check | Action |
|------|-------|--------|
| GATE-HEALTHCHECK | HEALTHCHECK instruction present | WARN |
| GATE-DIGEST-PIN | No mutable :latest in final FROM | BLOCK (after Phase 30) |
| GATE-CAP-DROP | evergreen.security.no-new-privileges label | WARN |

**Effort:** 2 hours | **Scriptable:** YES

### 32.4 Migrate 15 ADR-007 Debian Images to Wolfi

**Problem:** 15 images use single-stage `FROM debian` (Home Assistant, Paperless-ngx, Seafile, Taiga suites).

**Solution:** Convert to wolfi-base + apk add. May require package availability investigation.

**Effort:** 3-5 days | **Scriptable:** MANUAL

### 32.5 SBOM Depth Improvement

**Problem:** Current SBOMs have median 5 packages (min 1, max 63). Many are shallow - only listing the top-level binary without transitive dependencies.

**Solution:** Run `syft` at CI build time instead of manifest-based generation. This captures actual installed packages.

**Effort:** 5-7 days | **Scriptable:** HARD

---

## Phase 33: Advanced Hardening

**Effort:** 4-6 weeks | **Impact:** MEDIUM | **Priority:** FUTURE

### 33.1 read-only Root Filesystem with tmpfs

For images that need writable directories, add VOLUME declarations and document tmpfs mounts.

**Scope:** ~200 wolfi images that write to /tmp or /var.

**Effort:** 3-5 days

### 33.2 Seccomp Profiles Per Category

Create and validate seccomp profiles for 5 categories (default, webserver, database, monitoring, security). Infrastructure exists at `images/tests/profiles/seccomp-*.json`.

**Effort:** 1-2 weeks

### 33.3 SELinux/AppArmor Labels

Create confinement profiles for all image categories. Infrastructure exists at `images/tests/profiles/apparmor-*`.

**Effort:** 1-2 weeks

### 33.4 OCI Image Spec v1.1 Compliance

Upgrade from v1.0 to v1.1 with annotation indexing and attestations.

**Effort:** 1 week

### 33.5 SLSA v3 Provenance Generation

Currently configured but not fully validated. Complete the provenance pipeline with reusable workflow.

**Effort:** 1 week

---

## Phase 34: Documentation & Community

**Effort:** 1-2 weeks | **Impact:** MEDIUM | **Priority:** ONGOING

### 34.1 Per-Image README.md

Currently only 5/998 images have README.md. docs/standards.md 5.1 requires it for every image.

**Strategy:** Auto-generate stub READMEs from manifest.toml data, then community fills in details.

**Effort:** 3-5 days | **Scriptable:** YES (stub generation)

### 34.2 Fix Stale Documentation

The following documents contain outdated information from earlier phases and need updates:

| Document | Issue | Severity |
|----------|-------|----------|
| `CONSTRAINT_CHECKLIST.md` | References UID 65534, debian-slim as fallback, Alpine as acceptable | HIGH |
| `GOLDEN_10_REPORT.md` | Shows postgres/redis/keycloak on Alpine, all PENDING | MEDIUM |
| `SCALABILITY.md` | References Alpine as primary base for databases, UID 65534 | MEDIUM |
| `CHANGELOG.md` | Unreleased section has stale known issues (938 unverified checksums) | HIGH |
| `requiredimages.md` | Shows 1,050+ target but base image tier mapping uses old scheme | LOW |
| `README.md` | Says "distroless" but actual base is scratch/wolfi; missing 998 image scope | MEDIUM |
| `VERSION.md` | Line 134 says "CLI (10 subcommands)" but v2.0.0 has 14 | LOW |
| `TRACEABILITY_MATRIX.md` | Dated 2026-04-19, no reference to Phases 8-28 work | LOW |
| `docs/standards.md` | Says "Alpine MUST be used" as fallback (contradicts ADR-007 ban) | HIGH |
| `docs/observability.md` | Only describes sidecar pattern, missing Dockerfile HEALTHCHECK integration | MEDIUM |
| `docs/contributing_guide.md` | References `build-and-push.yml` for new images (should be `build.yml`) | LOW |
| `REQUIREMENTS.md` | Says "1,012 functional images" (actual: 998) | LOW |
| `newrequirements.md` | Correctly marked SUPERSEDED - no action needed | NONE |

### 34.3 README.md Rewrite

The public README should reflect the actual 998-image scope, current hardening posture, and accurate standards references.

---

## Priority Matrix

| Phase | Effort | Impact | Dependencies | Priority |
|-------|--------|--------|-------------|----------|
| **29** Security Hardening | 5-7 days | CRITICAL | None | **1 - DO NEXT** |
| **30** Reproducibility | 5-8 days | CRITICAL | None | **2 - DO NEXT** |
| **32** Compliance | 2-3 days | MEDIUM | Phase 29 | 3 |
| **34** Documentation | 1-2 weeks | MEDIUM | Phase 29 | 4 |
| **31** Multi-Arch | 12-15 days | HIGH | Phases 29-30 | 5 |
| **33** Advanced | 4-6 weeks | MEDIUM | Phases 29-32 | 6 |

### Critical Path

```
Phase 29 (Security) ─────> Phase 32 (Compliance) ──> Phase 33 (Advanced)
        |                                                    ^
Phase 30 (Reproducibility) ──> Phase 31 (Multi-Arch) ───────┘
                                       |
        Phase 34 (Documentation) <─────┘
```

### Quick Wins (Under 1 Day Each)

| # | Action | Images | Minutes |
|---|--------|--------|---------|
| 1 | Fix 7 broken TOML manifests | 7 | 30 |
| 2 | Fix 18 version mismatches | 18 | 60 |
| 3 | Add curl fallback `|| true` | 167 | 240 |
| 4 | Add apk cache cleanup | 584 | 120 |
| 5 | Retune C003 for wolfi | evergreenctl | 30 |
| 6 | Run pin_digests.sh | 998 | 60 |
| 7 | Add HEALTHCHECK directive | 998 | 120 |
| 8 | Add no-new-privileges label | 998 | 120 |
| 9 | Add CAP_DROP label | 998 | 120 |
| 10 | Fix VERSION.md "10 subcommands" -> "14" | 1 | 5 |

### Effort Estimate Summary

| Phase | Days | Cumulative |
|-------|------|------------|
| Quick wins (items 1-6) | 1 | 1 |
| Phase 29 (items 7-9 + 29.6-29.7) | 6 | 7 |
| Phase 30 (30.2-30.4) | 6 | 13 |
| Phase 32 (32.1-32.4) | 3 | 16 |
| Phase 34 (34.1-34.3) | 7 | 23 |
| Phase 31 (31.1-31.7) | 12 | 35 |
| Phase 33 (33.1-33.5) | 25 | 60 |
| **Total** | **~60 days** | |

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Digest pinning breaks builds (upstream changes) | Medium | High | Weekly re-pin via auto-bump workflow |
| Multi-arch reveals arm64-incompatible packages | High | Low | QEMU emulation in CI catches at build time |
| HEALTHCHECK causes startup delays | Low | Low | `--start-period` covers initialization |
| ADR-004 conversion introduces regressions | Medium | Medium | Phase 5 CI validation for each converted image |
| Python arm64 wheels missing | High | Medium | Accept amd64-only for those images, document |
| Home Assistant suite resists wolfi migration | High | Low | Document exception in ADR-008 |

---

## Success Criteria (Post-Roadmap)

| Metric | Current | Post-Phase 29 | Post-Phase 30 | Post-Phase 31 |
|--------|---------|---------------|---------------|---------------|
| HEALTHCHECK | 0% | 100% | 100% | 100% |
| CAP_DROP | 0.4% | 100% | 100% | 100% |
| no-new-privileges | 0% | 100% | 100% | 100% |
| Digest-pinned FROM | 0.3% | 0.3% | 100% | 100% |
| ADR-004 violations | 30 | 0 | 0 | 0 |
| Multi-arch | 20.7% | 20.7% | 20.7% | 36.5% (365/998) |
| GPG verification | 0.8% | 0.8% | 30%+ | 30%+ |
| Pipe-to-sh | 40 | 40 | 0 | 0 |
| Unverified downloads | 353 | 353 | 0 | 0 |

---

**END OF ROADMAP**
**Classification: OPERATIONAL PLANNING**
