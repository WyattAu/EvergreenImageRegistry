# Parity Closure Roadmap

> **Created:** July 2026  
> **Baseline:** v32.0.0, Phase 116, 708 active images  
> **Reference:** [Comparison Matrix](docs/comparison-matrix.md)  
> **Goal:** Close competitive gaps against Chainguard, Red Hat UBI, and Google Distroless

---

## Executive Summary

The comparison matrix identified **10 competitive gaps** between EIR and industry-leading providers. This roadmap closes
them in **5 layers over 7 phases**, prioritizing security impact, then supply chain trust, then compliance, then scale.

| Layer            | Phases    | Timeline | Gap Closure                             |
| ---------------- | --------- | -------- | --------------------------------------- |
| **Foundation**   | P117-P118 | ~4 weeks | Signing, SLSA, SBOM, CycloneDX          |
| **Hardening**    | P119-P120 | ~8 weeks | 100+ images from repack → scratch/wolfi |
| **Supply Chain** | P121      | ~3 weeks | Mirror completion, CVE auto-remediation |
| **Compliance**   | P122      | ~6 weeks | FIPS, CIS, STIG automation              |
| **Scale**        | P123      | ~4 weeks | s390x/ppc64le, reproducible builds      |

**Target End State:** EIR achieves feature parity with Chainguard free tier on all 10 gaps, with 100+ truly hardened
images.

---

## Gap Register

> Priority: **P0** = security blocker, **P1** = competitive disadvantage, **P2** = nice-to-have

| ID  | Gap                          | Priority | Current State                    | Target State                           | Competitor Benchmark              |
| --- | ---------------------------- | -------- | -------------------------------- | -------------------------------------- | --------------------------------- |
| G1  | Hardened image coverage      | P0       | 10/708 (1.4%)                    | 100+ (14%+)                            | Chainguard: 100% distroless       |
| G2  | Cosign signing integrated    | P0       | Workflow exists, not in pipeline | Every build signs every image          | Chainguard: All signed            |
| G3  | SLSA provenance integrated   | P0       | Workflow exists, not in pipeline | SLSA L3 on all builds                  | Chainguard: SLSA L3               |
| G4  | SBOM auto-generation         | P0       | 714 stale SPDX files             | Auto-generated per build, both formats | Chainguard: SPDX + CycloneDX      |
| G5  | CVE remediation SLA          | P1       | None (community)                 | Documented policy + auto-rebuild       | Chainguard: 7d/14d                |
| G6  | Compliance automation        | P1       | Plans + scripts, not certified   | Automated scans, documented evidence   | Red Hat: FIPS/STIG certified      |
| G7  | Docker Hub mirror completion | P1       | 85/369 (23%)                     | 369/369 (100%)                         | N/A (EIR-unique)                  |
| G8  | Multi-arch expansion         | P2       | amd64 + arm64                    | + s390x + ppc64le                      | Red Hat: 4 archs; Google: 6 archs |
| G9  | Reproducible builds          | P2       | Docker layer caching             | apko-based deterministic builds        | Chainguard: apko + cosign         |
| G10 | CycloneDX SBOM format        | P2       | SPDX only                        | SPDX + CycloneDX                       | Chainguard: Both formats          |

---

## Layer 1: Foundation (Supply Chain Trust)

> **Goal:** Every image built by CI is signed, has provenance, and has an auto-generated SBOM in both formats.  
> **Dependencies:** None — this is the foundation everything else builds on.

### Phase 117: Signing & Provenance Integration

**Gaps Closed:** G2 (Cosign), G3 (SLSA)  
**Estimated Effort:** 2 weeks  
**Depends On:** Nothing

#### Tasks

| ID    | Task                                                 | Description                                                                                                                                                         | Verification                                          | Effort |
| ----- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------ |
| 117.1 | **Merge signing into `_build-reusable.yml`**         | After each `docker push`, run `cosign sign --keyless` on the pushed digest. Replace the standalone `sign-images.yml` workflow with an inline step in the build job. | `cosign verify` on 10 sample images returns ✅        | 3 days |
| 117.2 | **Merge SLSA provenance into `_build-reusable.yml`** | Generate SLSA v1 provenance attestation using `slsa-github-generator` after each build. Attach as cosign attestation.                                               | `cosign download attestation` shows SLSA v1 predicate | 3 days |
| 117.3 | **Add provenance verification job**                  | Post-build job that verifies SLSA provenance for all built images. Fails CI if provenance is missing.                                                               | CI job runs and passes on nightly build               | 1 day  |
| 117.4 | **Remove standalone signing workflows**              | Delete `sign-images.yml`, `slsa-provenance.yml` (standalone), `sbom-attestation.yml` (standalone). Their logic is now inline.                                       | No orphaned workflows; no duplicate runs              | 1 day  |
| 117.5 | **Document verification process**                    | Add `docs/verifying-images.md` with `cosign verify` and `cosign verify-attestation` commands for users.                                                             | Documentation published; CI links to it               | 1 day  |

#### Success Criteria

- [ ] Every image pushed to GHCR has a cosign signature (keyless, via Sigstore OIDC)
- [ ] Every image has a SLSA v1 provenance attestation
- [ ] `cosign verify ghcr.io/wyattau/evergreenimageregistry/<any-image>:latest` succeeds
- [ ] `cosign verify-attestation --type slsaprovenance` succeeds
- [ ] No separate signing workflows — all inline in build pipeline
- [ ] Verification documentation published

---

### Phase 118: SBOM Modernization

**Gaps Closed:** G4 (Auto-generation), G10 (CycloneDX)  
**Estimated Effort:** 2 weeks  
**Depends On:** Phase 117 (uses cosign attestations)

#### Tasks

| ID    | Task                                   | Description                                                                                                            | Verification                                          | Effort   |
| ----- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | -------- |
| 118.1 | **Add Syft to build runner**           | Install Syft in the CI runner as a post-build step. Generate SBOM from the built image (not from Dockerfile analysis). | `syft` binary available in CI                         | 0.5 days |
| 118.2 | **Generate SPDX per image**            | After `docker push`, run `syft scan -o spdx-json` on the pushed image. Save as cosign attestation.                     | `cosign verify-attestation --type spdxjson` succeeds  | 1 day    |
| 118.3 | **Generate CycloneDX per image**       | After `docker push`, run `syft scan -o cyclonedx-json` on the pushed image. Save as cosign attestation.                | `cosign verify-attestation --type cyclonedx` succeeds | 1 day    |
| 118.4 | **Auto-update `sbom.spdx.json` files** | During build, commit updated SBOMs back to the repo via auto-bump bot. Keeps `images/<name>/sbom.spdx.json` fresh.     | SBOM files have current build date                    | 2 days   |
| 118.5 | **Add SBOM validation gate**           | Lint job that validates all `sbom.spdx.json` files are valid SPDX 2.3 and less than 30 days old.                       | Lint fails if any SBOM is stale/invalid               | 1 day    |
| 118.6 | **Remove stale SBOMs**                 | Delete the 714 hand-written/templated SBOM files. They will be auto-generated going forward.                           | Only auto-generated SBOMs exist                       | 0.5 days |
| 118.7 | **Add SBOM diff job**                  | Compare SBOM between consecutive builds. Alert on new packages or removed packages.                                    | CI job runs and reports SBOM diffs                    | 2 days   |

#### Success Criteria

- [ ] Every built image has both SPDX and CycloneDX SBOMs as cosign attestations
- [ ] `cosign verify-attestation --type spdxjson` and `--type cyclonedx` both succeed
- [ ] `images/<name>/sbom.spdx.json` files are auto-generated, not hand-written
- [ ] SBOM staleness check in lint pipeline
- [ ] SBOM diff alerts on package changes between builds

---

## Layer 2: Hardening (Security Posture)

> **Goal:** 100+ images are truly hardened (scratch/wolfi, non-root, no shell, verified at runtime).  
> **Dependencies:** Phase 117-118 complete (so hardened images are signed with provenance + SBOM).

### Phase 119: Critical Tier Hardening (Top 50)

**Gaps Closed:** G1 (Hardening coverage)  
**Estimated Effort:** 4 weeks  
**Depends On:** Phase 117, 118

#### Strategy

Not all 708 images can or should be hardened. Focus on the **101 critical tier** images first, prioritizing by:

1. **Infrastructure backbone** (already hardened): redis, nginx, traefik, prometheus, alertmanager, grafana,
   oauth2-proxy, keycloak, postgresql-16, mariadb
2. **Database layer**: mongodb, elasticsearch, valkey, etcd, consul, cockroachdb
3. **Message queue layer**: rabbitmq, nats, kafka, emqx
4. **Proxy/gateway layer**: envoy, haproxy, caddy, vaultwarden
5. **CI/CD layer**: gitea, forgejo, woodpecker-server, woodpecker-agent
6. **Observability layer**: node-exporter, blackbox-exporter, loki, tempo, thanos
7. **Security layer**: vault, step-ca, dex, kanidm

#### Hardening Patterns

| Pattern                       | Applicable To                                                | Method                                                        |
| ----------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------- |
| **Binary download → scratch** | Go/Rust static binaries (prometheus, traefik, grafana, etc.) | Download upstream binary, copy to scratch, USER 65532         |
| **Chainguard repack**         | Complex apps needing glibc (postgresql, mariadb)             | `FROM cgr.dev/chainguard/<app>` + COPY shim + non-root        |
| **Source build → scratch**    | C/C++ apps with static linking (redis)                       | Clone source, compile static, copy to scratch                 |
| **Wolfi apk-install**         | Apps needing shared libs but no full distro (nginx)          | `FROM cgr.dev/chainguard/wolfi-base` + `apk add` + USER 65532 |
| **Multi-stage distillation**  | Java apps (keycloak, elasticsearch)                          | FROM upstream → extract JRE + app → copy to wolfi-base        |

#### Tasks

| ID    | Task                        | Images                                                        | Verification                           | Effort |
| ----- | --------------------------- | ------------------------------------------------------------- | -------------------------------------- | ------ |
| 119.1 | Harden databases            | mongodb, elasticsearch, valkey, etcd, consul, cockroachdb (6) | Runtime smoke test per image           | 5 days |
| 119.2 | Harden message queues       | rabbitmq, nats, kafka, emqx, mosquitto (5)                    | Runtime smoke test                     | 4 days |
| 119.3 | Harden proxies/gateways     | envoy, haproxy, caddy, vaultwarden, traefik-whoami (5)        | HTTP response check                    | 3 days |
| 119.4 | Harden CI/CD                | gitea, forgejo, woodpecker-server, woodpecker-agent (4)       | HTTP/API check                         | 3 days |
| 119.5 | Harden observability        | node-exporter, blackbox-exporter, loki, tempo, thanos (5)     | Metrics endpoint check                 | 3 days |
| 119.6 | Harden security tools       | vault, step-ca, dex, kanidm, oauth2-proxy variants (5)        | HTTP/API check                         | 3 days |
| 119.7 | Harden remaining critical   | Top 20 remaining critical images by priority                  | Per-image smoke test                   | 5 days |
| 119.8 | Create hardening test suite | Automated smoke test harness for all hardened images          | `evergreenctl smoke --hardened` passes | 3 days |

#### Success Criteria

- [ ] 50+ images are `FROM scratch` or `FROM cgr.dev/chainguard/wolfi-base`
- [ ] 50+ images have `USER 65532:65532` (or app-specific non-root UID)
- [ ] 50+ images have no shell in final stage
- [ ] 50+ images pass runtime smoke tests (HTTP/TCP/metrics)
- [ ] Hardened images are signed, have SLSA provenance, and have dual-format SBOMs

---

### Phase 120: Standard Tier Selective Hardening (Next 50)

**Gaps Closed:** G1 (Hardening coverage — continued)  
**Estimated Effort:** 4 weeks  
**Depends On:** Phase 119

#### Tasks

| ID    | Task                             | Images                                                             | Verification     | Effort |
| ----- | -------------------------------- | ------------------------------------------------------------------ | ---------------- | ------ |
| 120.1 | Harden media applications        | jellyfin, navidrome, audiobookshelf, komga, calibre (5)            | HTTP check       | 3 days |
| 120.2 | Harden productivity apps         | nextcloud, paperless-ngx, n8n, outline, planka (5)                 | HTTP check       | 3 days |
| 120.3 | Harden network tools             | cloudflared, wireguard, pihole, adguardhome, unbound (5)           | Service check    | 3 days |
| 120.4 | Harden monitoring exporters      | 10+ Prometheus exporters (postgres-exporter, redis-exporter, etc.) | Metrics endpoint | 4 days |
| 120.5 | Harden dev tools                 | gitea-runner, code-server, lazydocker, dockge (5)                  | HTTP check       | 3 days |
| 120.6 | Harden remaining top-50 standard | By download count / SIS usage                                      | Per-image check  | 4 days |
| 120.7 | Document hardening cookbook      | `docs/hardening-guide.md` with patterns and templates              | Published        | 2 days |

#### Success Criteria

- [ ] 100+ total hardened images (10 existing + 50 Phase 119 + 50 Phase 120)
- [ ] Hardening cookbook published with reusable patterns
- [ ] `evergreenctl audit --hardened` shows 100+ images passing hardening checks

---

## Layer 3: Supply Chain Resilience

> **Goal:** Complete Docker Hub mirror, automated CVE detection, and auto-rebuild pipeline.  
> **Dependencies:** Phase 117-118 (signing + SBOM for attestation).

### Phase 121: Mirror Completion & CVE Auto-Remediation

**Gaps Closed:** G5 (CVE SLA), G7 (Mirror completion)  
**Estimated Effort:** 3 weeks  
**Depends On:** Phase 117, 118

#### Tasks

| ID    | Task                                       | Description                                                                                                                                            | Verification                                        | Effort |
| ----- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- | ------ |
| 121.1 | **Complete Docker Hub mirror**             | Fix `mirror_all.py` script (GHCR naming issue resolved). Run for remaining 284 upstreams. Update all Dockerfiles.                                      | 0 Docker Hub FROM lines remain in active images     | 3 days |
| 121.2 | **Add mirror freshness check**             | CI job that verifies all mirror images are < 7 days old. Auto-pulls and pushes if stale.                                                               | CI job runs nightly, mirrors refreshed              | 1 day  |
| 121.3 | **Enhance Trivy scanning**                 | Upgrade `daily-security-scan.yml` to scan ALL images (not just critical). Parse results into structured JSON.                                          | Daily scan covers 708 images, results in SARIF      | 2 days |
| 121.4 | **Add Grype scanning alongside Trivy**     | Run both Trivy and Grype. Deduplicate findings. Store unified results.                                                                                 | Both scanners run, dedup logic verified             | 1 day  |
| 121.5 | **Define CVE remediation policy**          | Document policy: Critical = rebuild within 7 days, High = 14 days, Medium = 30 days. Write to `docs/security-policy.md`.                               | Policy published and referenced in README           | 1 day  |
| 121.6 | **Implement auto-rebuild on critical CVE** | When Trivy finds CRITICAL CVE on an image: (1) check if upstream fix exists, (2) if yes, auto-create PR bumping upstream version, (3) trigger rebuild. | End-to-end test: inject fake CVE, verify PR created | 3 days |
| 121.7 | **Add CVE dashboard**                      | GitHub Pages site showing CVE counts per image, trends over time, remediation status.                                                                  | Dashboard updates daily with scan results           | 2 days |
| 121.8 | **Add upstream version watcher expansion** | Expand `upstream-watch.yml` from 20 to 100 images. Check for new upstream releases daily.                                                              | PR created within 24h of upstream release           | 2 days |

#### Success Criteria

- [ ] 0 active Dockerfiles reference Docker Hub directly (all mirrored)
- [ ] Mirror freshness check passes nightly
- [ ] Daily CVE scan covers all 708 images with Trivy + Grype
- [ ] CVE remediation policy documented
- [ ] Auto-rebuild triggers on critical CVE detection
- [ ] CVE dashboard live with trend data
- [ ] Upstream version watcher covers top 100 images

---

## Layer 4: Compliance Automation

> **Goal:** Automated compliance scanning and evidence generation for FIPS, CIS, and STIG.  
> **Dependencies:** Phase 117-118 (signing + SBOM for evidence), Phase 119-120 (hardened images as baseline).

### Phase 122: Compliance Scanning & Evidence

**Gaps Closed:** G6 (Compliance)  
**Estimated Effort:** 6 weeks  
**Depends On:** Phase 119 (hardened baseline images)

#### Tasks

| ID    | Task                                      | Description                                                                                                                                              | Verification                                   | Effort |
| ----- | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- | ------ |
| 122.1 | **FIPS 140-2/3 readiness scan**           | For each hardened image: verify OpenSSL config, check for non-FIPS algorithms, verify FIPS-capable base. Use `openssl fips` self-test.                   | Report per image: FIPS-ready / not-ready / N/A | 3 days |
| 122.2 | **FIPS implementation for top 30 images** | For the 30 images with FIPS plans in `compliance/fips/`: build FIPS variants using wolfi-fips base or OpenSSL FIPS module.                               | `OPENSSL_FIPS=1` self-test passes in container | 7 days |
| 122.3 | **CIS benchmark automation**              | Write CIS Docker benchmark scanning script. Run against hardened images. Store results in `compliance/cis/results/`.                                     | CIS scan runs in CI, results stored as JSON    | 3 days |
| 122.4 | **STIG hardening profiles**               | For images with STIG requirements: apply STIG-aligned configurations (SSH disabled, unnecessary packages removed, file permissions hardened).            | STIG scanner passes on profile-applied images  | 5 days |
| 122.5 | **Compliance evidence pipeline**          | CI job that collects all compliance artifacts (FIPS self-tests, CIS scans, STIG results, SBOMs, signatures) into a compliance evidence bundle per image. | Evidence bundle downloadable per image         | 3 days |
| 122.6 | **Compliance dashboard**                  | GitHub Pages site showing compliance status per image (FIPS/CIS/STIG), evidence links, gap analysis.                                                     | Dashboard live, updates with CI                | 3 days |
| 122.7 | **ATO controls mapping**                  | Map EIR controls to NIST 800-53 control families. Document in `compliance/ato/controls-mapping.md`.                                                      | Mapping reviewed and published                 | 3 days |
| 122.8 | **Document compliance limitations**       | Honest documentation of what EIR compliance provides vs what requires external certification. Write to `docs/compliance-posture.md`.                     | Published, referenced in README                | 1 day  |

#### Success Criteria

- [ ] 30 images have FIPS-ready variants
- [ ] CIS benchmark scan runs nightly on hardened images
- [ ] STIG profiles applied to security-critical images
- [ ] Compliance evidence bundle auto-generated per image
- [ ] Compliance dashboard live
- [ ] NIST 800-53 controls mapping published
- [ ] Limitations documented honestly

> **Note:** EIR cannot _certify_ FIPS/STIG/SOC2 — that requires accredited third-party auditors. What we CAN do is
> generate the evidence and documentation that makes certification faster and cheaper if pursued.

---

## Layer 5: Scale & Maturity

> **Goal:** Expand architecture support, achieve reproducible builds, and reach operational maturity.  
> **Dependencies:** All previous layers.

### Phase 123: Architecture Expansion & Reproducibility

**Gaps Closed:** G8 (Multi-arch), G9 (Reproducible builds)  
**Estimated Effort:** 4 weeks  
**Depends On:** Phase 121 (mirrors complete — needed for cross-arch pulls)

#### Tasks

| ID    | Task                                      | Description                                                                                                      | Verification                                  | Effort |
| ----- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------ |
| 123.1 | **Add s390x to multi-arch builds**        | Enable QEMU s390x emulation for critical tier. Test builds.                                                      | `docker manifest inspect` shows s390x entry   | 3 days |
| 123.2 | **Add ppc64le to multi-arch builds**      | Enable QEMU ppc64le emulation for critical tier. Test builds.                                                    | `docker manifest inspect` shows ppc64le entry | 3 days |
| 123.3 | **Evaluate apko for reproducible builds** | Spike: convert 5 hardened images from Dockerfile to `apko.yaml`. Compare determinism (same input → same digest). | 5 images build reproducibly with apko         | 5 days |
| 123.4 | **Migrate hardened images to apko**       | If spike succeeds, migrate all 100+ hardened images to apko-based builds. Keep Dockerfiles for non-hardened.     | Hardened images have deterministic digests    | 7 days |
| 123.5 | **Add build provenance verification**     | Verify that apko-built images match their `apko.yaml` source. Use cosign attestations to prove build source.     | Verification script passes on all apko images | 2 days |
| 123.6 | **Document architecture support matrix**  | Update README with per-image architecture support table.                                                         | Published, auto-generated from CI             | 1 day  |

#### Success Criteria

- [ ] Critical tier images available on amd64, arm64, s390x, ppc64le
- [ ] 100+ hardened images build reproducibly via apko
- [ ] Same `apko.yaml` + same package versions → same image digest
- [ ] Architecture support matrix published and auto-updated

---

## Phase Dependency Graph

```
Layer 1: Foundation
┌─────────────────────────────────────────┐
│  P117: Signing & Provenance (2 weeks)   │
│  └── P118: SBOM Modernization (2 weeks) │
└──────────────┬──────────────────────────┘
               │
               ▼
Layer 2: Hardening
┌─────────────────────────────────────────┐
│  P119: Critical Tier (4 weeks)          │
│  └── P120: Standard Tier (4 weeks)      │
└──────────────┬──────────────────────────┘
               │
Layer 3: Supply Chain      │   Layer 4: Compliance
┌────────────────────┐     │     ┌────────────────────┐
│ P121: Mirror + CVE │     │     │ P122: FIPS/CIS/STIG│
│ (3 weeks)          │←────┼────▶│ (6 weeks)          │
└────────┬───────────┘     │     └────────┬───────────┘
         │                 │              │
         ▼                 ▼              ▼
         ┌─────────────────────────────────┐
         │  Layer 5: Scale                 │
         │  P123: Arch + Reproducible (4w) │
         └─────────────────────────────────┘
```

---

## Milestone Summary

| Milestone                      | Version | Phases    | Weeks | Cumulative | Hardened Images | Key Deliverable                             |
| ------------------------------ | ------- | --------- | ----- | ---------- | --------------- | ------------------------------------------- |
| **M1: Trusted Pipeline**       | v33.0.0 | P117-P118 | 4     | 4          | 10              | Every image signed + provenance + dual SBOM |
| **M2: Hardened Core**          | v34.0.0 | P119      | 4     | 8          | 60              | 50+ new hardened critical images            |
| **M3: Hardened Catalog**       | v35.0.0 | P120      | 4     | 12         | 110             | 100+ hardened images total                  |
| **M4: Supply Chain Resilient** | v36.0.0 | P121      | 3     | 15         | 110             | 0 Docker Hub deps, auto-CVE rebuild         |
| **M5: Compliance Ready**       | v37.0.0 | P122      | 6     | 21         | 110             | FIPS/CIS/STIG evidence per image            |
| **M6: Scale Parity**           | v38.0.0 | P123      | 4     | 25         | 110+            | 4 architectures, reproducible builds        |

---

## Gap Closure Tracking

| Gap                               | Phase(s)   | Milestone | Status         |
| --------------------------------- | ---------- | --------- | -------------- |
| G1: Hardened coverage (10 → 100+) | P119, P120 | M3        | 🔴 Not started |
| G2: Cosign signing integrated     | P117       | M1        | 🔴 Not started |
| G3: SLSA provenance integrated    | P117       | M1        | 🔴 Not started |
| G4: SBOM auto-generation          | P118       | M1        | 🔴 Not started |
| G5: CVE remediation SLA           | P121       | M4        | 🔴 Not started |
| G6: Compliance automation         | P122       | M5        | 🔴 Not started |
| G7: Docker Hub mirror (85 → 369)  | P121       | M4        | 🔴 Not started |
| G8: Multi-arch (2 → 4+)           | P123       | M6        | 🔴 Not started |
| G9: Reproducible builds           | P123       | M6        | 🔴 Not started |
| G10: CycloneDX SBOM               | P118       | M1        | 🔴 Not started |

**Legend:** 🔴 Not started | 🟡 In progress | 🟢 Complete

---

## Risk Register

| Risk                                                   | Probability | Impact | Mitigation                                                                 |
| ------------------------------------------------------ | ----------- | ------ | -------------------------------------------------------------------------- |
| apko spike fails (G9)                                  | Medium      | Low    | Keep Dockerfile-based builds; reproducibility is P2                        |
| s390x/ppc64le QEMU too slow for CI                     | High        | Medium | Only build those archs for critical tier; community tier stays amd64+arm64 |
| Docker Hub rate limits block mirror completion         | Medium      | High   | Run mirror from GHCR-authed runner; batch with retries                     |
| FIPS validation requires certified crypto module       | High        | Medium | Document as "FIPS-ready" not "FIPS-certified"; use wolfi-fips base         |
| Hardening 100 images takes longer than estimated       | Medium      | Medium | Prioritize by SIS usage; defer low-traffic images                          |
| Cosign keyless signing has service availability issues | Low         | High   | Fallback to cosign with stored key if Fulcio/Rekor down                    |
| SBOM generation slows CI pipeline                      | Medium      | Low    | Generate SBOMs post-push (non-blocking); async attestation                 |

---

## Definition of Done

A gap is considered **closed** when ALL of the following are true:

1. **Implementation:** The feature/task is built and functional
2. **Verification:** Automated tests or CI checks validate the feature
3. **Documentation:** The feature is documented in the appropriate `docs/` file
4. **Integration:** The feature is integrated into the main CI/CD pipeline (not standalone)
5. **Measurement:** A metric or dashboard tracks the feature's ongoing health
6. **Gap Matrix Updated:** The comparison matrix `docs/comparison-matrix.md` reflects the closure

---

## Appendix A: Effort Estimation Methodology

- Estimates are in **engineering days** (1 day = ~6 productive hours)
- Estimates assume a single contributor with deep familiarity with the codebase
- Parallelizable tasks are noted but not de-risked in estimates
- No estimate includes context-switching overhead or meetings
- Estimates do not include the time to debug test failures or CI issues (add ~30% buffer)
- **Total estimated effort:** ~125 engineering days (~25 weeks at 5 days/week)

## Appendix B: Competitor Parity Targets

| Gap | When Closed | EIR Status            | Competitor                   | Full Parity?                      |
| --- | ----------- | --------------------- | ---------------------------- | --------------------------------- |
| G1  | M3 (P120)   | 100+ hardened         | Chainguard: 2000+ distroless | ❌ Partial (10% of catalog)       |
| G2  | M1 (P117)   | All signed            | Chainguard: All signed       | ✅ Yes                            |
| G3  | M1 (P117)   | SLSA on all           | Chainguard: SLSA L3          | ⚠️ Close (L2 vs L3)               |
| G4  | M1 (P118)   | Auto-gen both         | Chainguard: Both formats     | ✅ Yes                            |
| G5  | M4 (P121)   | 7d/14d policy         | Chainguard: Contractual SLA  | ⚠️ Close (policy vs contract)     |
| G6  | M5 (P122)   | Evidence + automation | Red Hat: Certified           | ❌ Partial (evidence vs cert)     |
| G7  | M4 (P121)   | 100% mirrored         | N/A (EIR-unique)             | ✅ Yes                            |
| G8  | M6 (P123)   | 4 architectures       | Google: 6; Red Hat: 4        | ⚠️ Close (missing riscv64, arm32) |
| G9  | M6 (P123)   | apko reproducible     | Chainguard: apko + cosign    | ✅ Yes                            |
| G10 | M1 (P118)   | SPDX + CycloneDX      | Chainguard: Both             | ✅ Yes                            |

**Full parity achieved:** G2, G4, G7, G9, G10 (5/10)  
**Near parity achieved:** G3, G5, G8 (3/10)  
**Partial parity:** G1, G6 (2/10) — these require scale or external certification beyond EIR's scope

---

## Appendix C: Tools & Technologies

| Tool                  | Purpose                            | Phase | Already in Use?               |
| --------------------- | ---------------------------------- | ----- | ----------------------------- |
| **cosign** (Sigstore) | Image signing, attestation         | P117  | ✅ Yes (standalone workflows) |
| **Syft** (Anchore)    | SBOM generation (SPDX + CycloneDX) | P118  | ❌ No                         |
| **Trivy** (Aqua)      | Vulnerability scanning             | P121  | ✅ Yes (nightly scan)         |
| **Grype** (Anchore)   | Vulnerability scanning             | P121  | ❌ No                         |
| **apko** (Chainguard) | Reproducible OCI image builds      | P123  | ❌ No                         |
| **QEMU**              | Cross-architecture emulation       | P123  | ✅ Yes (arm64 builds)         |
| **GitHub Actions**    | CI/CD pipeline                     | All   | ✅ Yes                        |
| **GHCR**              | Container registry                 | All   | ✅ Yes                        |
| **Docker buildx**     | Multi-arch builds                  | P123  | ✅ Yes (critical + standard)  |
| **OpenSSF Scorecard** | Security posture scoring           | P122  | ❌ No                         |
