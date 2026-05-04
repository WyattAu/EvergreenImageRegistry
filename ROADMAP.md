# Evergreen Image Registry - Roadmap

| Attribute | Value |
|-----------|-------|
| Version | 2.0.0 |
| Updated | 2026-05-03 |
| Status | ACTIVE |
| Post-Phase | 34 |

---

## Current Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Total images | 998 | — |
| HEALTHCHECK | 100% (997/997) | DONE |
| CAP_DROP label | 100% (997/997) | DONE |
| no-new-privileges | 100% (997/997) | DONE |
| read-only-rootfs label | 100% (997/997) | DONE |
| seccomp label | 100% (997/997) | DONE |
| Digest-pinned (final-stage) | 100% | DONE |
| Digest-pinned (all stages) | 73.6% (1485/2019) | Partial |
| Multi-arch (ARG TARGETARCH) | 32.2% (321/997) | Partial |
| TOML parse errors | 0 | DONE |
| Version mismatches | 0 | DONE |
| ADR-004 banned bases | 0 (all multi-stage) | DONE |
| C003 false positives | ~0 (retuned) | DONE |
| Pipe-to-sh | 1 | Nearly done |
| apk cache cleanup | 0 | DONE |
| Per-image README | 4/998 | NOT STARTED |
| CI gates | 0 | NOT STARTED |
| SBOM at build time | manifest-based | NOT STARTED |

---

## Achieved (Phases 28-34)

| Phase | Scope | Key Result |
|-------|-------|------------|
| 28 | Sovereign-to-Evergreen rebrand | Full rebrand |
| 29 | Security hardening | HEALTHCHECK, CAP_DROP, no-new-privileges, TOML fixes, version mismatches |
| 30 | Reproducibility | Digest pinning to 73.6% (final-stage 100%), apk cache cleanup |
| 31 | Multi-arch expansion | 207 → 321 images |
| 32 | Compliance tuning | C003 retuned (~0 FP), deploy UID fix |
| 33 | Advanced security labels | read-only-rootfs, seccomp labels on all images |
| 34 | README redesign | README.md rewrite completed |

Total changes across phases 28-34: ~2,105 files modified.

---

## Remaining Work

### Phase 35: CI Validation & Regression Fixes

**Effort:** 1-3 days | **Priority:** 1

2,105 file changes need a full rebuild to catch regressions introduced during hardening.

- Verify all 998 images still build
- Fix HEALTHCHECK regressions (curl in scratch images, wrong ports)
- Fix digest pin drift from upstream updates
- Fix 1 remaining pipe-to-sh image

### Phase 36: Remaining Digest Pinning

**Effort:** 2-4 hours | **Priority:** 2

Current: 73.6% (1485/2019 FROM refs). Remaining 534 refs:

- **39 upstream version refs** — pin specific versions (vaultwarden, influxdb, etc.)
- **5 :latest refs** — auth-gated upstreams, may need CI credentials
- **100 ${VERSION} refs** — build-time resolved via ARG, acceptable as-is
- **390 wolfi builder-stage refs** — intermediate stages, lower priority

### Phase 37: CI Gates

**Effort:** 2-4 hours | **Priority:** 3

| Gate | Check | Action |
|------|-------|--------|
| GATE-HEALTHCHECK | HEALTHCHECK instruction present | WARN |
| GATE-DIGEST-PIN | No mutable :latest in final FROM | WARN |
| GATE-SECURITY-LABELS | 4 security labels present (CAP_DROP, no-new-privileges, read-only-rootfs, seccomp) | WARN |

### Phase 38: Per-Image README Stubs

**Effort:** 1 day | **Priority:** 4

Only 4/998 images have README.md. Auto-generate stubs from manifest.toml data (version, description, exposed ports, health check path, upstream URL).

### Phase 39: SBOM at Build Time

**Effort:** 1-2 days | **Priority:** 5

Replace manifest-based SBOMs with `syft` at CI build time. Captures actual installed packages including transitive dependencies.

### Phase 40: Multi-Arch Hard Cases

**Effort:** 2-3 weeks | **Priority:** 6

| Category | Images | Challenge |
|----------|--------|-----------|
| C/C++ via QEMU | 40 | Cross-compilation toolchains, native dependencies |
| Python arm64 | 140 | Missing arm64 wheels for C-extension packages |

Easy wins (Java, Node, Go, Rust) are already done.

---

## Not Recommended

| Item | Reason |
|------|--------|
| Seccomp profiles per category | `runtime-default` is sufficient; per-profile gains are marginal |
| SELinux/AppArmor confinement | High effort for niche benefit; requires host-side policy |
| OCI v1.1 migration | Incremental over v1.0, no user-visible impact |
| LICENSE per image | SBOMs already capture license data |
| Migrate 15 debian images to wolfi | High regression risk (Home Assistant, Paperless-ngx, Seafile, Taiga suites) |

---

## Effort Summary

| Phase | Days | Cumulative |
|-------|------|------------|
| 35: CI validation | 1-3 | 1-3 |
| 36: Digest pinning | <1 | 2-3 |
| 37: CI gates | <1 | 2-4 |
| 38: README stubs | 1 | 3-5 |
| 39: SBOM at build time | 1-2 | 4-7 |
| 40: Multi-arch hard cases | 10-15 | 14-22 |

---

**END OF ROADMAP**
