# Evergreen Image Registry — Repack Image Migration Plan

## Executive Summary

**798 total images** → **75 already hardened** (9.4%) → **723 need migration** (90.6%)

All 723 images are **Tier 3 (Community)**. Tier 1 (87 critical) and Tier 2 (711 standard) images are already using scratch, wolfi-base, or distroless.

## Migration Categories

| Category | Count | Target Base | Effort | Strategy |
|----------|-------|-------------|--------|----------|
| Go binaries | ~200 | scratch | Low | Extract binary, copy to scratch |
| Static binaries | ~50 | scratch | Low | Extract binary, copy to scratch |
| Language runtimes (Python/Node/Java) | 51 | wolfi-base | Medium | Replace base, translate packages |
| Complex apps (databases, servers) | ~420 | wolfi-base | High | Binary extraction + shim |
| **Total** | **723** | | | |

## Phase 1: Go Binary Extraction (Week 1-2) — ~200 images

**Target:** Images that compile Go binaries with `CGO_ENABLED=0`

**Pattern:**

```dockerfile
# BEFORE (upstream repack)
FROM golang:1.23-bookworm AS builder
RUN go build -o /app
FROM ubuntu:22.04
COPY --from=builder /app /usr/local/bin/app
CMD ["app"]

# AFTER (hardened)
FROM scratch
COPY --from=builder /app /usr/local/bin/app
USER 65532
ENTRYPOINT ["/usr/local/bin/app"]
```

**Automated migration possible:** Yes — detect `go build` + `CGO_ENABLED=0` in builder, replace final stage with `scratch`.

**Estimated images:** ~200 (conservatively)

## Phase 2: Static Binary Extraction (Week 2-3) — ~50 images

**Target:** Images with statically compiled C/C++/Rust binaries

**Pattern:**

```dockerfile
# BEFORE
FROM debian:bookworm-slim AS builder
RUN apt-get install && make
FROM debian:bookworm-slim
COPY --from=builder /app /usr/local/bin/app

# AFTER
FROM scratch
COPY --from=builder /app /usr/local/bin/app
USER 65532
ENTRYPOINT ["/usr/local/bin/app"]
```

**Automated migration possible:** Yes — detect `-static` flag or musl target in build commands.

## Phase 3: Language Runtime Migration (Week 3-5) — 51 images

**Target:** Python, Node.js, Ruby, PHP, Java images

**Strategy:** Replace upstream base with wolfi-base, translate packages.

| Language | Current Base | Target Base | Key Changes |
|----------|-------------|-------------|-------------|
| Python | `python:3.x-slim` | `cgr.dev/chainguard/python` | apt→apk, pip packages |
| Node.js | `node:XX-slim` | `cgr.dev/chainguard/node` | apt→apk, npm packages |
| Ruby | `ruby:3.x-slim` | `cgr.dev/chainguard/ruby` | apt→apk, gem packages |
| Java | `eclipse/temurin:XX` | `cgr.dev/chainguard/openjdk-XX` | apt→apk |
| PHP | `php:8.x-apache` | `cgr.dev/chainguard/php` | apt→apk |

**Automated migration possible:** Partial — package name translation via `migrate_debian_to_wolfi.sh`

## Phase 4: Complex App Migration (Week 5-12) — ~420 images

**Target:** Databases, proxies, message queues, web apps

**Strategy:** Binary extraction from upstream image → wolfi-base

**Pattern:**

```dockerfile
# BEFORE
FROM upstream/app:latest
# Just re-tags upstream

# AFTER
FROM upstream/app:latest AS upstream
FROM cgr.dev/chainguard/wolfi-base
COPY --from=upstream /usr/local/bin/app /usr/local/bin/app
COPY --from=upstream /etc/app /etc/app
USER 65532
ENTRYPOINT ["/usr/local/bin/app"]
```

**Automated migration possible:** Partial — needs per-image analysis of file dependencies.

## Migration Priority Matrix

| Priority | Criteria | Images | Timeline |
|----------|----------|--------|----------|
| P0 | Tier 1 + Tier 2 | 0 (done) | Complete |
| P1 | Go binaries with CGO_ENABLED=0 | ~200 | Week 1-2 |
| P2 | Static binaries | ~50 | Week 2-3 |
| P3 | Language runtimes | 51 | Week 3-5 |
| P4 | Complex apps (databases) | ~100 | Week 5-8 |
| P5 | Complex apps (everything else) | ~320 | Week 8-12 |

## Success Criteria

| Metric | Current | 30-Day | 60-Day | 90-Day |
|--------|---------|--------|--------|--------|
| Scratch/wolfi/distroless final stages | 75 (9.4%) | 275 (34%) | 475 (60%) | 723 (91%) |
| CIS 4.4.3 pass rate (no shell) | ~10% | ~30% | ~50% | ~80% |
| CIS 4.4.1 pass rate (non-root) | ~40% | ~60% | ~80% | ~95% |
| C015 violations (no :latest) | ~300 | ~200 | ~100 | ~30 |

## Tools

| Tool | Purpose | Status |
|------|---------|--------|
| `migrate_debian_to_wolfi.sh` | apt→apk translation | ✅ Created |
| `smoke_test.sh` | Runtime validation | ✅ Created |
| `cis-gate.yml` | PR-level CIS checks | ✅ Created |
| `validate-parallel` | 20-constraint validation | ✅ Updated |

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Binary extraction breaks dependencies | Smoke test after each migration |
| Package name mismatches (apt→apk) | 60+ package mapping table in migration script |
| musl vs glibc compatibility | Test all dynamic binaries against wolfi |
| CI breakage during batch migration | Migrate in batches of 10, validate between batches |
| Upstream image changes break extraction | Pin upstream to digest, not tag |
