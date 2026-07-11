# Forward Roadmap: Production Hardening

> **Created:** July 2026  
> **Baseline:** v33.0.0, 708 active images, 65 real hardened, CI RED  
> **Philosophy:** Fix what's broken first. Harden what matters most. Ship iteratively.

---

## Current State (Brutally Honest)

### What's Working

| Item                       | Status | Detail                                                                   |
| -------------------------- | ------ | ------------------------------------------------------------------------ |
| 708 active images          | ✅     | All on GHCR, all have Dockerfiles                                        |
| 65 hardened images         | ✅     | scratch/wolfi + non-root + ENTRYPOINT + HEALTHCHECK                      |
| 85 Docker Hub mirrors      | ✅     | 256 Dockerfiles use GHCR mirrors                                         |
| Shim v2.0.0                | ✅     | 650 Dockerfiles reference it, binary on GHCR                             |
| Signing/SLSA/SBOM pipeline | ✅     | Inline in `_build-reusable.yml` (untested in CI yet)                     |
| Multi-arch QEMU            | ✅     | amd64, arm64, s390x, ppc64le configured                                  |
| Compliance scanners        | ✅     | `fips_scan.sh`, `cis_scan.sh` created                                    |
| Documentation              | ✅     | 7 docs (comparison, roadmap, security, compliance, hardening, verifying) |

### What's Broken

| Issue                              | Severity | Impact                                                      |
| ---------------------------------- | -------- | ----------------------------------------------------------- |
| **CI lint failing**                | 🔴 P0    | Blocks all merges, blocks nightly builds                    |
| **Build-on-push failing**          | 🔴 P0    | No CI builds running                                        |
| **Publish immutable tags failing** | 🔴 P0    | No version tags published                                   |
| **13 stub images**                 | 🟡 P1    | scratch/wolfi base but no app binary — clutter              |
| **323 Docker Hub deps**            | 🟡 P1    | Rate limit risk in batch builds                             |
| **305 archived images**            | 🟡 P2    | Each needs manual upstream lookup                           |
| **Smoke test step broken**         | 🟡 P1    | References unresolved variable in report job                |
| **Entrypoint validator**           | 🟡 P1    | False positives on mariadb/postgresql (inherit upstream EP) |
| **SBOM files stale**               | 🟡 P2    | 714 hand-written files, not auto-generated                  |

---

## Phase Priority Order

```
Phase 1: Fix CI (BLOCKING)
    ↓
Phase 2: Validate Pipeline (signing/SBOM/SLSA actually works)
    ↓
Phase 3: Clean Up (stubs, entrypoint validator, smoke test)
    ↓
Phase 4: Harden More Images (from 65 to 100+)
    ↓
Phase 5: Docker Hub Mirror Completion
    ↓
Phase 6: SIS Migration Finish
```

---

## Phase 1: Fix CI

> **Goal:** All CI checks pass. Nightly builds run green.  
> **Estimated Effort:** 1-2 days  
> **Blocks:** Everything

### 1.1 Fix entrypoint validator false positives

**Problem:** `validate_entrypoint_pattern.py` reports mariadb and postgresql-16 as missing ENTRYPOINT. These are
Chainguard repacks that inherit the upstream's ENTRYPOINT.

**Fix:** Add `chainguard-repack` exemption pattern. Images that `FROM cgr.dev/chainguard/*` inherit upstream ENTRYPOINT
— this is valid.

### 1.2 Fix smoke test step in report job

**Problem:** The `report` job in `_build-reusable.yml` has a smoke test step that references `${{ matrix.images }}` and
`${{ steps.resolve-tag.outputs.TAG }}`, but these are only available in the `build` job (matrix strategy). The report
job doesn't have matrix context.

**Fix:** Remove the smoke test, runtime test, and security scan from the report job. They belong in the build job (or a
separate post-build job that downloads the built-images artifact).

### 1.3 Fix publish-immutable-tags workflow

**Problem:** Failing — need to check the actual error.

### 1.4 Verify nightly build triggers correctly

**Problem:** Build-on-push is failing. Need to verify the `_build-reusable.yml` inline signing step doesn't break the
build.

---

## Phase 2: Validate Supply Chain Pipeline

> **Goal:** Confirm that cosign signing, Syft SBOM generation, and SLSA provenance actually work end-to-end in CI.  
> **Estimated Effort:** 2-3 days  
> **Depends On:** Phase 1

### 2.1 Trigger a test build

Manually trigger `build-on-demand.yml` for 3-5 images. Verify:

- [ ] Image builds and pushes to GHCR
- [ ] `cosign sign` succeeds (keyless via OIDC)
- [ ] `syft scan` generates SPDX SBOM from the actual image
- [ ] `syft scan` generates CycloneDX SBOM
- [ ] `cosign attest` attaches SPDX SBOM
- [ ] `cosign attest` attaches CycloneDX SBOM
- [ ] `cosign attest` attaches SLSA provenance
- [ ] `cosign verify` succeeds on the pushed image
- [ ] `cosign verify-attestation --type spdxjson` succeeds
- [ ] `cosign verify-attestation --type cyclonedx` succeeds
- [ ] `cosign verify-attestation --type slsaprovenance` succeeds

### 2.2 Fix any issues found

Common anticipated issues:

- cosign OIDC token not available (need `id-token: write` permission — already added)
- Syft can't scan multi-arch manifest (may need to scan specific platform)
- SLSA provenance JSON malformed (hand-written template may have issues)
- Grype installation fails (wrong action version)

### 2.3 Document the verified workflow

Update `docs/verifying-images.md` with actual verified output examples.

---

## Phase 3: Clean Up

> **Goal:** Remove stubs, fix validators, make CI reliable.  
> **Estimated Effort:** 2-3 days  
> **Depends On:** Phase 1

### 3.1 Archive stub images

13 images are scratch/wolfi-based but have no real application:

| Image                        | Action  | Reason                                |
| ---------------------------- | ------- | ------------------------------------- |
| `aarch64-unknown-linux-musl` | Archive | Build tool, not a deployable image    |
| `amd64`                      | Archive | Duplicate of architecture base        |
| `gitlab`                     | Archive | No real GitLab binary                 |
| `grub`                       | Archive | Bootloader, not container-appropriate |
| `musl`                       | Archive | Build tool                            |
| `pulsar`                     | Archive | Stub, no real Pulsar                  |
| `scratch-base`               | Archive | Meta image, not deployable            |
| `static-c`                   | Archive | Build tool                            |
| `windows-exporter`           | Archive | Wrong platform                        |
| `wolfi-gcc`                  | Archive | Build tool                            |
| `wolfi-node`                 | Archive | Build tool                            |
| `wolfi-python`               | Archive | Build tool                            |

### 3.2 Fix entrypoint validator

Add exemption patterns for:

- `chainguard-repack`: Images FROM `cgr.dev/chainguard/*` inherit upstream ENTRYPOINT
- `base-image`: Meta images (health-shim, wolfi-base variants) that serve as build bases

### 3.3 Move smoke test to correct job

The runtime smoke test, security scan, and metrics test are in the `report` job which doesn't have matrix context. Move
them to a new `verify` job that:

- Downloads built-image references artifact
- Pulls images from GHCR
- Runs smoke tests
- Runs Trivy scan
- Reports results

### 3.4 Regenerate SBOMs

Delete all 714 hand-written `sbom.spdx.json` files. They will be auto-generated by Syft during the build pipeline.

---

## Phase 4: Harden More Images

> **Goal:** Increase from 65 to 100+ real hardened images.  
> **Estimated Effort:** 1-2 weeks (iterative)  
> **Depends On:** Phase 1, 3

### Priority Images to Harden Next

Focus on images actually used in SIS deployments:

| Image       | Current State    | Hardening Method                                | Priority |
| ----------- | ---------------- | ----------------------------------------------- | -------- |
| vaultwarden | Repack (debian)  | Source-build or static binary → scratch         | High     |
| forgejo     | Repack           | Binary download → scratch (Go binary)           | High     |
| valkey      | Repack           | Binary download → scratch                       | High     |
| etcd        | Repack (quay.io) | Binary download → scratch (Go binary)           | High     |
| dex         | Repack           | Binary download → scratch (Go binary)           | Medium   |
| step-ca     | Repack           | Binary download → scratch (Go binary)           | Medium   |
| rabbitmq    | Repack           | Chainguard repack if available, else wolfi-base | Medium   |
| cloudflared | Repack           | Binary download → scratch (Go binary)           | Medium   |
| mosquitto   | Repack           | wolfi-base + apk                                | Medium   |
| n8n         | Repack           | Needs Node.js runtime — use distroless nodejs   | Low      |

### Hardening Process (Per Image)

1. Identify binary download URL (GitHub releases)
2. Write scratch Dockerfile with shim
3. Build locally
4. Run smoke test (TCP/HTTP check)
5. Push to GHCR
6. Verify entrypoint validator passes
7. Move to next image

---

## Phase 5: Docker Hub Mirror Completion

> **Goal:** Mirror all remaining 323 Docker Hub upstreams.  
> **Estimated Effort:** 3-5 days (automated script, runs unattended)  
> **Depends On:** Phase 1

### Approach

The `mirror_all.py` script works but is slow (pull + tag + push per image). Run it unattended:

```bash
# Run in background with logging
nohup python3 -u scripts/mirror_all.py > /tmp/mirror.log 2>&1 &
```

The script:

1. Finds all Docker Hub FROM lines not yet mirrored
2. Pulls each from Docker Hub
3. Tags as `ghcr.io/.../mirror-<name>:latest`
4. Pushes to GHCR
5. Updates Dockerfiles

### Known Issues to Fix

- "Does not provide any platform" error on some pushes → use `docker buildx imagetools create` instead
- Timeout on large images (gitlab, pytorch) → skip these, handle manually

---

## Phase 6: SIS Migration Finish

> **Goal:** All SIS stacks use EIR images.  
> **Estimated Effort:** 1 week  
> **Depends On:** Phase 4

### Remaining SIS Stacks

| Stack                    | Status  | Blocker                                |
| ------------------------ | ------- | -------------------------------------- |
| immich                   | Blocked | Custom postgres with vector extensions |
| infra-webhook            | Blocked | Custom build, needs investigation      |
| Remaining utility stacks | TODO    | Need compose file updates              |

### Process

1. List all SIS stacks on TrueNAS
2. For each: identify current images, find EIR equivalents
3. Update compose files
4. Deploy and verify
5. Commit to SIS repo

---

## Metrics & Success Criteria

| Metric                 | Current | Target | Phase |
| ---------------------- | ------- | ------ | ----- |
| CI lint passing        | ❌      | ✅     | P1    |
| CI build passing       | ❌      | ✅     | P1    |
| cosign verify works    | ❓      | ✅     | P2    |
| SBOM attestation works | ❓      | ✅     | P2    |
| SLSA provenance works  | ❓      | ✅     | P2    |
| Stub images            | 13      | 0      | P3    |
| Hardened images        | 65      | 100+   | P4    |
| Docker Hub deps        | 323     | <50    | P5    |
| SIS stacks on EIR      | 11      | 15+    | P6    |
