# Evergreen Image Registry - Roadmap

| Attribute | Value |
|-----------|-------|
| Version | 26.1.0 |
| Updated | 2026-05-05 |
| Status | MAINTENANCE |
| Phases | 0-45 + ongoing polish |

---

## Current State (v26.1.0)

| Metric | Value | Status |
|--------|-------|--------|
| Total images | 998 | — |
| HEALTHCHECK (real) | 569/997 (57.1%) | DONE |
| HEALTHCHECK NONE | 428/997 (42.9%) | Expected (scratch/no-shell) |
| Security labels (4) | 100% | DONE |
| OCI labels (title) | 100% (997/997) | DONE |
| OCI labels (description) | 100% (997/997) | DONE |
| OCI labels (source) | 100% (997/997) | DONE |
| OCI labels (version) | 100% (997/997) | DONE |
| Digest-pinned | 75.4% (94.7% immutable) | DONE |
| Multi-arch (ARG TARGETARCH) | 637/997 (63.9%) | DONE |
| Multi-arch CI matrix | 632 images | DONE |
| Per-image README | 100% (997/997) | DONE |
| SBOM | 100% manifest + build-time syft | DONE |
| CI gates | Active (C001-C010 + size) | DONE |
| TOML validity | 100% | DONE |
| Workflows | 10 files | DONE |
| Anti-patterns | 0 across all 997 images | DONE |
| Layers (avg RUN/image) | 1.0 (953 total) | DONE |

---

## Completed Phases (0-45)

| Phase | What | Key Metric |
|-------|------|------------|
| 0 | Foundation | Project structure, base images |
| 1-27 | Iterative build | 998 images, labels, healthchecks |
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
| 42 | Quality audit | RUN consolidation (837 images, 1790 layers), curl\|sh (8), eval (6), apt-get (13), sudo (1), .dockerignore (997), cross-ref fixes (11) |
| 43 | Security scan + multi-arch | 68 new multi-arch, 504 OCI descriptions, 10 shellcheck fixes, daily-scan.yml 4 bug fixes |
| 44 | SLSA + Cosign + gates | SLSA v3 provenance, Cosign OIDC signing, verify gates fixed (C002/C003/C004 skip logic), Zstd compression, 7 k8s multi-arch |
| 45 | Infrastructure polish | Concurrency groups, image size tracking, 103 multi-arch (635 total), CIFuzz, Docker Hub push, upstream version checker |
| 46 | Healthchecks + labels + CI fix | 12 service healthchecks (vault/traefik/nginx/coredns/prometheus/loki/minio/etcd/nats/influxdb/consul/gitea), 49 OCI titles, secrets-in-if CI fix, rust-static multi-arch |

---

## Remaining Work

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

**ALL PLANNED PHASES COMPLETE — project in maintenance mode.**
