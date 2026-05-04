# Evergreen Image Registry - Roadmap

| Attribute | Value |
|-----------|-------|
| Version | 23.0.0 |
| Updated | 2026-05-04 |
| Status | COMPLETE |
| Phases | 28-41 |

---

## Current State (v23.0.0)

| Metric | Value | Status |
|--------|-------|--------|
| Total images | 998 | — |
| HEALTHCHECK | 100% (997/997) | DONE |
| Security labels (4) | 100% | DONE |
| Digest-pinned | 75.4% (94.7% immutable) | DONE |
| Multi-arch (ARG TARGETARCH) | 457/997 (45.8%) | DONE |
| Multi-arch CI matrix | 458 images | DONE |
| Per-image README | 100% (997/997) | DONE |
| SBOM | 100% manifest + build-time syft | DONE |
| CI gates | Active (all pass) | DONE |
| TOML validity | 100% | DONE |

---

## Completed Phases (28-41)

| Phase | What | Key Metric |
|-------|------|------------|
| 28 | Rebrand | 0 sovereign refs |
| 29 | Security Hardening | HEALTHCHECK 100%, CAP_DROP 100% |
| 30 | Reproducibility | 75.4% digest-pinned |
| 31 | Multi-arch (easy wins) | 321 images |
| 32 | Compliance | C003 retuned |
| 33 | Advanced labels | read-only-rootfs, seccomp |
| 34 | README redesign | Professional 128-line README |
| 35 | CI gates | 997/997 pass |
| 36 | Digest pinning | 17 more upstreams pinned |
| 37 | Per-image READMEs | 997/997 |
| 38 | SBOM at build time | syft integration |
| 39 | C/C++ multi-arch | 21 images |
| 40 | Python multi-arch | 115 safe images |
| 41 | Matrix expansion | 458 images in CI |

---

## Remaining Work

### Known Gaps

- 5 auth-gated `:latest` FROM refs (dependabot, lancedb, scylladb, tigergraph x2)
- 100 `${VERSION}` build-time FROM refs (acceptable)
- 39 specific upstream version FROM refs (some may need re-pinning)
- 11 Python NEEDS INVESTIGATION images (vllm, deepspeed, comfyui, etc.)
- 540 images without multi-arch support (mostly C-extension Python, specialized tools)

### Future Considerations (Low Priority)

- SBOM depth improvement (syft captures actual packages)
- Seccomp profiles per category (runtime-default sufficient)
- SELinux/AppArmor (niche benefit)
- OCI v1.1 compliance (incremental)

### NOT Recommended

| Item | Reason |
|------|--------|
| LICENSE per image | SBOMs already capture license info |
| Migrate 15 debian images to wolfi | High regression risk |
| Per-image docker-compose files | Unmaintainable at 998 scale |

---

**ALL PLANNED PHASES COMPLETE — project in maintenance mode.**
