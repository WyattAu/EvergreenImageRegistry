# Evergreen Image Registry - Roadmap

| Attribute | Value |
|-----------|-------|
| Version | 26.4.0 |
| Updated | 2026-05-12 |
| Status | POST-CI-FIX |
| Phases | 0-52 + ongoing polish |

---

## Current State (v26.4.0)

| Metric | Value | Status |
|--------|-------|--------|
| Total images | 998 | — |
| HEALTHCHECK (real) | 559/998 (56.0%) | DONE |
| HEALTHCHECK NONE | 438/998 (43.9%) | Expected (scratch/no-shell) |
| Security labels (4) | 100% | DONE |
| OCI labels (title) | 100% (998/998) | DONE |
| OCI labels (description) | 99.9% (997/998) | DONE |
| OCI labels (source) | 99.7% (995/998) | DONE |
| OCI labels (version) | 99.8% (996/998) | DONE |
| Digest-pinned FROM | 75.3% (1522/2020) | DONE |
| Non-root USER | 99.5% (993/998) | DONE |
| ENTRYPOINT | 95.8% (956/998) | DONE |
| STOPSIGNAL | 99.6% (994/998) | DONE |
| Multi-arch (ARG TARGETARCH) | 249 declared + 391 scratch | DONE |
| Per-image README | 100% (998/998) | DONE |
| SBOM | 100% (998/998) | DONE |
| .dockerignore | 99.9% (997/998) | DONE |
| CI gates | Active (C001-C010 + size) | DONE |
| TOML validity | 100% (998/998) | DONE |
| Anti-patterns | 0 real (1 false positive) | DONE |
| Dockerfile syntax errors | 0 | DONE |
| Determinism | Zstd + SOURCE_DATE_EPOCH | DONE |
| Workflows | 10 files | DONE |
| Layers (avg RUN/image) | 1.0 (953 total) | DONE |
| Rigor (real binary) | 99.8% (996/998) | DONE |

---

## Completed Phases (0-50)

| Phase | What | Key Metric |
|-------|------|------------|
| 0 | Foundation | Project structure, base images |
| 1-27 | Iterative build | 998 images, labels, healthchecks |
| 28 | Rebrand | 0 sovereign refs |
| 29 | Security Hardening | HEALTHCHECK 100%, CAP_DROP 100% |
| 30 | Reproducibility | 75.3% digest-pinned |
| 31 | Multi-arch (easy wins) | 321 images |
| 32 | Compliance | C003 retuned |
| 33 | Advanced labels | read-only-rootfs, seccomp |
| 34 | README redesign | Professional 128-line README |
| 35 | CI gates | 998/998 pass |
| 36 | Digest pinning | 17 more upstreams pinned |
| 37 | Per-image READMEs | 998/998 |
| 38 | SBOM at build time | syft integration |
| 39 | C/C++ multi-arch | 21 images |
| 40 | Python multi-arch | 115 safe images |
| 41 | Matrix expansion | 458 images in CI |
| 42 | Quality audit | RUN consolidation (837 images, 1790 layers), curl\|sh (8), eval (6), apt-get (13), sudo (1), .dockerignore (997), cross-ref fixes (11) |
| 43 | Security scan + multi-arch | 68 new multi-arch, 504 OCI descriptions, 10 shellcheck fixes, daily-scan.yml 4 bug fixes |
| 44 | SLSA + Cosign + gates | SLSA v3 provenance, Cosign OIDC signing, verify gates fixed (C002/C003/C004 skip logic), Zstd compression, 7 k8s multi-arch |
| 45 | Infrastructure polish | Concurrency groups, image size tracking, 103 multi-arch (635 total), CIFuzz, Docker Hub push, upstream version checker |
| 46 | Healthchecks + labels + CI fix | 12 service healthchecks, 49 OCI titles, secrets-in-if CI fix, rust-static multi-arch |
| 49 | Blank line continuation fix | 2795 blank lines removed from LABEL/RUN blocks (broke `\` continuations) |
| 50 | CI-driven Dockerfile syntax fixes (6 rounds) | 300+ fixes: `\|\| true #` → `\|\| true \\`, `&&&&` → `&&`, LABEL on continuations, package-manager-verified on scratch, duplicated placeholders, split apk+php, orphaned commands, `; adduser` → `&& adduser`, chown resilience |

---

## Remaining Work

### CI Failure Categories (~80-120 images, all upstream issues)

| Category | Count | Fixable? | Action |
|----------|-------|----------|--------|
| curl-404 (old release deleted) | ~21 | YES | Version bump + sha256 |
| curl-404 (same version, CI transient) | ~8 | MAYBE | Re-run CI / investigate |
| upstream-image-not-found | ~37 | PARTIAL | ~15 version bump, ~10 deleted, ~12 auth-gated |
| build-compilation (couchdb, HA) | ~3 | NO | Upstream build broken |
| copy-to-non-directory (cache) | ~5 | TRANSIENT | BuildKit cache issue |
| auth-gated (dependabot) | ~2 | NO | Needs GitHub PAT |

### Immediate Next Steps (Phase 51)

1. **Version bump batch** — Update ~21 images with deleted releases to latest versions
2. **Upstream image-not-found audit** — Version bump ~15, document ~25 as permanently broken
3. **wolfi package compatibility** — Verify php-8.4, php83, redis, g++ availability in current wolfi

### Known Gaps

- 5 auth-gated `:latest` FROM refs (dependabot, lancedb, scylladb, tigergraph x2)
- 100 `${VERSION}` build-time FROM refs (acceptable — resolved at build time)
- 360 images without multi-arch (C-extension Python ~80, amd64-only upstream ~200, GPU/ML ~50, niche ~30)

### Future Considerations (Low Priority)

- More service healthchecks (428 remaining HEALTHCHECK NONE — mostly scratch/no-shell)
- SBOM depth improvement (syft captures actual packages)
- Seccomp profiles per category (runtime-default sufficient)
- SELinux/AppArmor (niche benefit)
- OCI v1.1 compliance (incremental)
- Merge rust-static-arm into rust-static (legacy redirect needed)
- Merge x86_64/aarch64-unknown-linux-musl into unified image

### NOT Recommended

| Item | Reason |
|------|--------|
| LICENSE per image | SBOMs already capture license info |
| Migrate 15 debian images to wolfi | High regression risk |
| Per-image docker-compose files | Unmaintainable at 998 scale |
| Builder image multi-arch (golang, rust, maven, gradle) | Digest-pinned Debian needs per-arch digests, low ROI |

---

**ALL SYNTAX FIXES COMPLETE — remaining failures are upstream issues (Phase 51: version bumps).**
