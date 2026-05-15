# =============================================================================

# PHASE 1: SUPPLY CHAIN INTEGRITY - Detailed Execution Plan

# =============================================================================

# Version: 1.0.0

# Status: PENDING

# Author: Nexus (Principal Systems Architect)

# Date: 2026-04-19

#

# ABSTRACT: Supply chain security is the #1 risk for military contractors and

# evergreen infrastructure operators. This phase implements cryptographic

# verification of all downloaded artifacts (SHA256 checksums for ~107 images

# using curl-based multi-stage builds), enforces Cosign keyless signing with

# Fulcio/Rekor transparency logs, generates SLSA v3 provenance attestations,

# produces signed SBOMs in SPDX format, creates a hermetic CI build

# environment, and removes the dangerous `--ignore-unfixed` flag from Trivy

# CVE scanning. Phase 0 must pass all quality gates before this phase begins.

# =============================================================================

## Table of Contents

1. [Current State Assessment](#1-current-state-assessment)
2. [Task Inventory](#2-task-inventory)
3. [Detailed Task Specifications](#3-detailed-task-specifications)
4. [Quality Gates](#4-quality-gates)
5. [Risk Register](#5-risk-register)
6. [Rollback Procedures](#6-rollback-procedures)
7. [Success Metrics](#7-success-metrics)

---

## 1. Current State Assessment

### 1.1 Download Patterns in Current Dockerfiles

Every multi-stage scratch/distroless Dockerfile follows the same pattern in the `downloader` stage:

```dockerfile
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
RUN curl -fsSL "https://example.com/release/v1.0/binary.tar.gz" -o /binary.tar.gz && \
    tar -xzf /binary.tar.gz -C / && rm /binary.tar.gz && chmod +x /binary
```

**Critical gap:** No checksum verification after download. An attacker who compromises the download URL, performs a MITM
attack, or compromises the CDN can inject malicious binaries into every image.

### 1.2 Image Categories Requiring Checksum Verification

| Category                    | Count    | Download Method                                   | Checksum Needed    | Source of Truth                 |
| --------------------------- | -------- | ------------------------------------------------- | ------------------ | ------------------------------- |
| Scratch (curl download)     | ~85      | `curl -fsSL` from GitHub releases / project sites | SHA256             | Upstream release page + GPG sig |
| Distroless (curl download)  | ~7       | `curl -fsSL` from GitHub releases                 | SHA256             | Upstream release page           |
| Debian-slim (apt install)   | ~87      | `apt-get install`                                 | N/A (apt verifies) | Debian package signing          |
| Wolfi                       | ~13      | `apk add` from Chainguard                         | N/A (apk verifies) | Chainguard signing              |
| Other/Official              | ~12      | Mixed                                             | Varies             | Per-image                       |
| **Total needing checksums** | **~107** |                                                   |                    |                                 |

### 1.3 Current CI Pipeline Security Posture

| Security Feature      | Status  | Location                                                                                |
| --------------------- | ------- | --------------------------------------------------------------------------------------- |
| Trivy CVE scanning    | PARTIAL | `build.yml:438` — uses `--ignore-unfixed=false` (good) but no `.trivyignore` management |
| Grype CVE scanning    | PARTIAL | `build.yml:448` — secondary scan, no unfixed filtering                                  |
| Cosign signing        | PARTIAL | `build.yml:506-530` — key-based OR keyless, but no Fulcio/Rekor documented              |
| SBOM generation       | PARTIAL | `build.yml:532-561` — syft generates SPDX, cosign attests                               |
| SLSA provenance       | PARTIAL | `build.yml:270` — `--attest "type=provenance,mode=max"` on push                         |
| TruffleHog scanning   | WEAK    | `build.yml:184-189` — `continue-on-error: true`, scans full repo only                   |
| Secret scanning       | MISSING | No pre-commit hook, no per-Dockerfile scan                                              |
| Hermetic build        | MISSING | CI runner uses ad-hoc tool installation                                                 |
| Checksum verification | MISSING | Zero Dockerfiles verify downloaded artifacts                                            |
| `.trivyignore`        | MISSING | No exception management for known CVEs                                                  |

### 1.4 Key Vulnerabilities

| ID     | Vulnerability                                | Impact                                | Images Affected |
| ------ | -------------------------------------------- | ------------------------------------- | --------------- |
| SC-001 | No checksum verification on downloads        | CRITICAL — arbitrary code execution   | ~107            |
| SC-002 | TruffleHog `continue-on-error: true`         | HIGH — secrets may pass undetected    | All             |
| SC-003 | No hermetic CI environment                   | MEDIUM — build reproducibility risk   | All             |
| SC-004 | No SLSA provenance verification in consumers | MEDIUM — supply chain trust gap       | All             |
| SC-005 | No `.trivyignore` governance                 | LOW — no documented exception process | All             |

---

## 2. Task Inventory

### Dependency Graph (Topological Order)

```
Phase 0 (all gates passed)
    |
    +--> T1.1.1 (CHECKSUMS files) ──> T1.1.2 (Update Dockerfiles to verify)
    |
    +--> T1.2.1 (Cosign keyless signing) ──> T1.2.2 (SLSA v3 provenance)
    |                                   ──> T1.3.2 (SBOM attestation)
    |
    +--> T1.3.1 (TruffleHog integration) ──> Independent
    |
    +--> T1.4.1 (Remove ignore-unfixed) ──> Independent
    |
    +--> T1.4.2 (Hermetic build env) ──> Independent
```

### Parallel Execution Opportunities

```
Stream A: Checksum Verification (T1.1.1 -> T1.1.2) — BLOCKING on T0.3.1
Stream B: Signing & Provenance (T1.2.1 -> T1.2.2, T1.3.2) — Independent
Stream C: Secret Scanning (T1.3.1) — Independent
Stream D: Trivy Hardening (T1.4.1) — Independent
Stream E: Hermetic CI (T1.4.2) — Independent
```

Streams B, C, D, and E can all execute in parallel. Stream A depends on Phase 0 completion (specifically T0.3.1
multi-stage conversion).

### Effort Estimate Summary

| Task      | Estimated Hours | Parallel?                 |
| --------- | --------------- | ------------------------- |
| T1.1.1    | 16              | No (sequential per image) |
| T1.1.2    | 8               | After T1.1.1              |
| T1.2.1    | 4               | Yes                       |
| T1.2.2    | 4               | After T1.2.1              |
| T1.3.1    | 2               | Yes                       |
| T1.3.2    | 2               | After T1.2.1              |
| T1.4.1    | 2               | Yes                       |
| T1.4.2    | 8               | Yes                       |
| **Total** | **46**          | **~30 hours wall-clock**  |

---

## 3. Detailed Task Specifications

### 3.1 T1.1.1: Create per-image CHECKSUMS files with SHA256

#### Problem Analysis

Currently, 107 images download binaries via `curl -fsSL` with zero integrity verification. The download pattern in every
Dockerfile `downloader` stage is:

```dockerfile
RUN curl -fsSL "<URL>" -o /artifact.tar.gz && \
    tar -xzf /artifact.tar.gz -C / && rm /artifact.tar.gz && chmod +x /binary
```

If the URL serves compromised content (MITM, CDN breach, GitHub release hijack), the binary is blindly extracted and
copied into the final image. This is the highest-severity supply chain risk.

#### Solution: Per-Image CHECKSUMS File

Create a `CHECKSUMS` file alongside each Dockerfile that downloads a binary. The file format:

```
# CHECKSUMS for <image_name>
# Generated: 2026-04-19
# Source: https://github.com/<org>/<repo>/releases/download/v<ver>/
#
# Format: SHA256  <filename>
<sha256>  <filename>
```

Example for `images/nginx/CHECKSUMS`:

```
# CHECKSUMS for nginx
# Generated: 2026-04-19
# Source: https://nginx.org/download/
#
# Format: SHA256  <filename>
e6a57c7b2e5e1b716b7e4e6781c5c2b8b7e6e5c5b4a3a2b1e0d9c8b7a6e5f4  nginx-1.27.1.tar.gz
```

#### Checksum Acquisition Strategy

| Source Type                 | Acquisition Method                           | Trust Level                           |
| --------------------------- | -------------------------------------------- | ------------------------------------- |
| GitHub Releases             | Download SHA256SUMS file from release assets | HIGH (signed by GitHub)               |
| Project website             | Scrape checksum from official download page  | MEDIUM (verify with GPG if available) |
| Upstream provides `.sha256` | Download companion hash file                 | HIGH                                  |
| No upstream checksum        | Compute from verified binary, document risk  | LOW (ADR required)                    |

#### Implementation Steps

1. **Inventory all images with curl downloads** (script):

   ```bash
   grep -rl 'curl -fsSL' images/*/Dockerfile | \
     sed 's|images/||' | sed 's|/Dockerfile||' | sort > /tmp/images-with-curl.txt
   ```

2. **Create checksum extraction script** (`scripts/generate_checksums.sh`):

   ```bash
   #!/bin/bash
   # For each image, extract download URL from Dockerfile,
   # fetch upstream checksum, write CHECKSUMS file
   IMAGE="$1"
   DOCKERFILE="images/${IMAGE}/Dockerfile"

   # Extract URL from curl command
   URL=$(grep -oP 'curl -fsSL "\K[^"]+' "$DOCKERFILE")

   # Extract filename from URL
   FILENAME=$(basename "$URL")

   # Try to fetch upstream checksum
   # ... (logic varies by source)

   # Write CHECKSUMS file
   cat > "images/${IMAGE}/CHECKSUMS" << EOF
   # CHECKSUMS for ${IMAGE}
   # Generated: $(date -I)
   # Source: ${URL}
   #
   # Format: SHA256  <filename>
   ${SHA256}  ${FILENAME}
   EOF
   ```

3. **Handle multi-binary downloads**: Some Dockerfiles have fallback patterns:

   ```dockerfile
   curl -fsSL "...tar.gz" -o /binary.tar.gz && \
       tar -xzf /binary.tar.gz ... || \
   curl -fsSL "...binary" -o /binary
   ```

   Each URL needs its own checksum entry.

4. **Validate all checksums**: After generating, verify each checksum by downloading the artifact and comparing.

5. **Document exceptions**: Images where no upstream checksum exists require ADR justification.

#### Verification Criteria

- [ ] Every image directory containing a Dockerfile with `curl -fsSL` has a `CHECKSUMS` file
- [ ] Every `CHECKSUMS` file contains the SHA256 hash of the downloaded artifact
- [ ] Source URL for each checksum is documented
- [ ] `scripts/generate_checksums.sh` is idempotent (re-running produces same output)
- [ ] Manual spot-check: download artifact, verify hash matches CHECKSUMS file

---

### 3.2 T1.1.2: Update all Dockerfiles to verify checksums

#### Problem Analysis

Having CHECKSUMS files is useless if Dockerfiles don't use them. Every `curl` download must be followed by `sha256sum`
verification that fails the build on mismatch.

#### Solution: Inline Checksum Verification

**Pattern A: Single download (most common)**

```dockerfile
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

ARG EXPECTED_SHA256=deadbeef...
RUN curl -fsSL "https://example.com/binary.tar.gz" -o /binary.tar.gz && \
    echo "${EXPECTED_SHA256}  /binary.tar.gz" | sha256sum -c - && \
    tar -xzf /binary.tar.gz -C / && rm /binary.tar.gz && chmod +x /binary
```

**Pattern B: Download with fallback (current pattern)**

```dockerfile
ARG EXPECTED_SHA256_TGZ=deadbeef...
ARG EXPECTED_SHA256_BIN=cafebabe...
RUN curl -fsSL "...tar.gz" -o /binary.tar.gz && \
    echo "${EXPECTED_SHA256_TGZ}  /binary.tar.gz" | sha256sum -c - && \
    tar -xzf /binary.tar.gz -C / && rm /binary.tar.gz && chmod +x /binary
# Fallback removed — build fails if primary download fails checksum
```

**Decision:** Remove the fallback pattern entirely. If the primary download fails checksum verification, the build MUST
fail. Silent fallback to a different URL is itself a security risk.

#### Implementation Steps

1. **Create Dockerfile update script** (`scripts/add_checksum_verification.sh`):
   - Parse each Dockerfile for `curl -fsSL` lines
   - Read corresponding CHECKSUMS file
   - Insert `ARG EXPECTED_SHA256=...` before the FROM instruction
   - Insert `sha256sum -c` after the `curl` line
   - Remove fallback `|| curl ...` patterns

2. **Handle debian-slim apt images**: These use `apt-get install` which has its own GPG verification. Add a comment
   documenting this:

   ```dockerfile
   # NOTE: apt-get packages are verified by Debian GPG signing
   # No additional checksum verification needed for apt packages
   ```

3. **Test updated Dockerfiles**: Build each image and verify:
   - Correct checksum: build succeeds
   - Incorrect checksum: build fails with clear error message

4. **Error message format**:
   ```dockerfile
   RUN echo "${EXPECTED_SHA256}  /binary.tar.gz" | sha256sum -c - || \
       { echo "CHECKSUM VERIFICATION FAILED for binary.tar.gz"; \
         echo "Expected: ${EXPECTED_SHA256}"; \
         echo "Actual: $(sha256sum /binary.tar.gz | cut -d' ' -f1)"; \
         exit 1; }
   ```

#### Verification Criteria

- [ ] Every `curl -fsSL` in every Dockerfile is followed by `sha256sum -c`
- [ ] Build with correct checksum succeeds
- [ ] Build with incorrect checksum fails with descriptive error
- [ ] Error message includes expected vs actual hash
- [ ] No fallback `|| curl` patterns remain
- [ ] Failing image count is zero

---

### 3.3 T1.2.1: Implement Cosign keyless signing with Fulcio/Rekor

#### Problem Analysis

Current `build.yml:506-530` has signing logic but it falls back to key-based signing when `COSIGN_PRIVATE_KEY` is not
set. Keyless signing using OIDC tokens from GitHub Actions provides stronger security properties:

- No long-lived private keys to manage or rotate
- Signatures bound to GitHub identity (repository + ref)
- Entries in Rekor transparency log provide tamper-evident audit trail
- Verifiers can confirm the signing identity without access to any secret

#### Solution: Enforce Keyless Signing

**Current state in `build.yml`:**

```yaml
- name: Sign images with Cosign
  env:
    COSIGN_PRIVATE_KEY: ${{ secrets.COSIGN_PRIVATE_KEY }}
    COSIGN_PASSWORD: ${{ secrets.COSIGN_PASSWORD }}
  run: |
    if [ -n "$COSIGN_PRIVATE_KEY" ]; then
      cosign sign --yes --key env://COSIGN_PRIVATE_KEY "${ref}"
    else
      cosign sign --yes "${ref}"
    fi
```

**Target state:**

```yaml
- name: Sign images with Cosign (keyless)
  run: |
    cosign sign --yes \
      --certificate-identity="${{ github.repository_owner }}" \
      --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
      "${ref}"
```

Keyless signing uses the GitHub Actions OIDC token (already available via `id-token: write` permission) to get a
certificate from Fulcio, and records the signature in Rekor's transparency log.

#### Implementation Steps

1. **Remove key-based signing path**: Delete the `COSIGN_PRIVATE_KEY` / `COSIGN_PASSWORD` environment variables and the
   conditional branch.

2. **Add identity annotations**: Bind signatures to the repository identity:

   ```bash
   cosign sign --yes \
     --certificate-identity="${{ github.server_url }}/${{ github.repository }}" \
     --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
     "${ref}"
   ```

3. **Update SBOM attestation** (T1.3.2 will also use keyless):

   ```bash
   cosign attest --yes \
     --certificate-identity="..." \
     --certificate-oidc-issuer="..." \
     --predicate "${SBOM}" --type spdxjson "${ref}"
   ```

4. **Create consumer verification documentation** (`docs/signing-verification.md`):

   ```bash
   # Verify image was signed by this repository
   cosign verify \
     --certificate-identity="https://github.com/WyattAu/EvergreenImageRegistry" \
     --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
     ghcr.io/wyattau/evergreenimageregistry/nginx:sha-abc123
   ```

5. **Test locally**: Use `cosign sign-blob` with a local key to simulate the flow before committing.

#### Verification Criteria

- [ ] `cosign verify` succeeds with certificate-identity and OIDC issuer flags
- [ ] Signature recorded in Rekor transparency log (queryable via `rekor-cli search`)
- [ ] Verification documentation complete with working examples
- [ ] No key-based signing fallback path exists
- [ ] Both sign and attest steps use keyless flow

---

### 3.4 T1.2.2: Generate SLSA v3 provenance attestations

#### Problem Analysis

The current build.yml already includes `--attest "type=provenance,mode=max"` on the push step (`build.yml:270`). This
uses Docker BuildKit's built-in provenance generation. However, this provenance:

1. Is generated by Docker Buildx, not by `slsa-github-generator`
2. May not meet SLSA v3 requirements (specifically, the builder identity may not be verifiable)
3. Is attached during push but not independently verifiable

SLSA v3 requires:

- **Source**: Identified by URI and digest -. **Builder**: Identified by trusted builder identity
- **Config**: Build configuration is reproducible
- **Parameters**: All build inputs are recorded

#### Solution: Use slsa-github-generator

Replace the BuildKit provenance with `slsa-github-generator` for stricter SLSA v3 compliance.

**Add to `build.yml` after the verify stage:**

```yaml
provenance:
  name: Generate SLSA Provenance
  needs: [discover, verify]
  if: github.event_name != 'pull_request' && github.ref == 'refs/heads/main'
  uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v1.9.0
  with:
    image: ${{ env.REGISTRY }}/${{ env.OWNER }}/${{ matrix.image }}
    digest: ${{ needs.verify.outputs.digest }}
  permissions:
    id-token: write
    contents: read
    packages: write
```

**Alternatively** (simpler approach): Use `cosign attest` with provenance predicate generated by
`slsa-github-generator`:

```yaml
- name: Generate SLSA provenance
  uses: slsa-framework/slsa-github-generator/actions/generate-container-provenance@v1.9.0
  with:
    image: ${{ env.REGISTRY }}/${{ env.OWNER }}/${{ matrix.image }}
```

#### Implementation Steps

1. **Evaluate current BuildKit provenance**: Run `slsa-verifier` against current images to determine compliance gap.

2. **Integrate slsa-github-generator**: Add provenance generation step to CI pipeline after build+verify stages.

3. **Verify provenance** with `slsa-verifier`:

   ```bash
   slsa-verifier verify-image \
     --source-uri github.com/WyattAu/EvergreenImageRegistry \
     --builder-id https://github.com/slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml \
     ghcr.io/wyattau/evergreenimageregistry/nginx:sha-abc123
   ```

4. **Create documentation** (`docs/slsa-provenance.md`): Consumer guide for verifying SLSA provenance.

#### Verification Criteria

- [ ] `slsa-verifier verify-image` succeeds for all built images
- [ ] Provenance includes source URI, commit digest, builder identity
- [ ] Provenance is attached via `cosign attest`
- [ ] Documentation includes consumer verification instructions
- [ ] SLSA level 3 compliance confirmed by `slsa-verifier`

---

### 3.5 T1.3.1: Integrate TruffleHog secret scanning

#### Problem Analysis

Current state (`build.yml:184-189`):

```yaml
- name: TruffleHog secret scanning
  uses: trufflehog/trufflehog@main
  continue-on-error: true # DANGEROUS: secrets pass silently
  with:
    extra_args: --only-verified
```

Problems:

1. `continue-on-error: true` means secrets can pass undetected
2. `uses: trufflehog/trufflehog@main` is unpinned (could be compromised)
3. Scans the entire repo, not specifically Dockerfiles and build context
4. No pre-commit hook for developer-time feedback

#### Solution: Hardened TruffleHog Integration

**Updated CI step:**

```yaml
- name: TruffleHog secret scanning (Dockerfiles)
  uses: trufflehog/trufflehog@v3.82.0 # PINNED VERSION
  continue-on-error: false # BLOCKING
  with:
    extra_args: --only-verified --no-update images/
```

**Pre-commit hook** (`.pre-commit-config.yaml`):

```yaml
repos:
  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.82.0
    hooks:
      - id: trufflehog
        args: [--only-verified, --no-update, images/]
```

**`.trufflehogignore`** (if needed):

```
# Only add entries with ADR justification
# Format: file or pattern
```

#### Implementation Steps

1. **Pin TruffleHog version**: Change `@main` to a specific release tag.

2. **Make blocking**: Remove `continue-on-error: true`.

3. **Scope to images directory**: Pass `images/` as target instead of scanning entire repo.

4. **Add pre-commit hook**: Install TruffleHog as a pre-commit hook for developer-time feedback.

5. **Test with known secret**: Temporarily add a test secret to verify detection, then remove.

#### Verification Criteria

- [ ] TruffleHog version is pinned (not `@main`)
- [ ] `continue-on-error` is `false` (blocking)
- [ ] Scan targets `images/` directory specifically
- [ ] Pre-commit hook runs on `git commit`
- [ ] Test with planted secret: scan detects and blocks

---

### 3.6 T1.3.2: Sign SBOMs with Cosign attestation

#### Problem Analysis

Current SBOM generation in `build.yml:532-561` uses `syft` to generate SPDX JSON and `cosign attest` to attach it.
However, it still uses the key-based signing path. This task aligns the SBOM attestation with the keyless signing flow
from T1.2.1.

#### Solution: Keyless SBOM Attestation

**Updated step:**

```yaml
- name: Generate and attest SBOMs (keyless)
  run: |
    while IFS= read -r ref; do
      [ -z "$ref" ] && continue
      SAFE=$(echo "$ref" | tr '/:' '_')
      SBOM="/tmp/sbom-${SAFE}.spdx.json"

      syft "${ref}" -o "spdx-json=${SBOM}" || continue

      cosign attest --yes \
        --certificate-identity="${{ github.server_url }}/${{ github.repository }}" \
        --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
        --predicate "${SBOM}" \
        --type spdxjson \
        "${ref}"
    done < /tmp/all-images.txt
```

#### Implementation Steps

1. **Remove key-based signing env vars** from SBOM attestation step.

2. **Add keyless identity parameters**: Same certificate-identity and OIDC issuer as T1.2.1.

3. **Verify SBOM retrieval**:
   ```bash
   cosign verify-attestation \
     --certificate-identity="..." \
     --certificate-oidc-issuer="..." \
     --type spdxjson \
     "${ref}" | jq .
   ```

#### Verification Criteria

- [ ] SBOM attestation uses keyless signing (no `COSIGN_PRIVATE_KEY`)
- [ ] `cosign verify-attestation` succeeds with identity verification
- [ ] SBOM content is valid SPDX JSON
- [ ] SBOM includes all packages in the image

---

### 3.7 T1.4.1: Remove ignore-unfixed from Trivy scan

#### Problem Analysis

The current `build.yml:438` already has `--ignore-unfixed=false`, which is correct. However, there is no `.trivyignore`
file to manage legitimate exceptions. When a CRITICAL CVE has no fix, the build will fail with no way to document and
manage the exception.

This is a governance problem: without an exception process, the pipeline will either:

- Fail permanently on unfixable CVEs (blocking all development)
- Force developers to disable scanning entirely (worst outcome)

#### Solution: Implement CVE Exception Governance

1. **Create `.trivyignore` with documented exceptions**:

   ```
   # .trivyignore
   # Each entry must have a corresponding ADR justification
   # Format: CVE-YYYY-NNNNN
   #
   # See .adrs/ for justification of each exception
   ```

2. **Add CVE exception documentation**: Each exception requires:
   - CVE ID and severity
   - Affected component and version
   - Why no fix is available
   - Compensating controls
   - Review date and owner

3. **Add automated exception expiry**: Exceptions expire after 90 days, forcing re-evaluation:

   ```yaml
   - name: Check .trivyignore expiry
     run: |
       # Scan .trivyignore for entries older than 90 days
       # Fail if any expired entries found
       python3 scripts/check_trivyignore_expiry.py
   ```

4. **Trivy configuration file** (`.trivy.yaml`):
   ```yaml
   severity:
     - CRITICAL
     - HIGH
   ignore-unfixed: false
   exit-code: 1
   format: table
   ```

#### Implementation Steps

1. **Audit current CVE landscape**: Run Trivy against all images to catalog unfixable CVEs.

2. **Create `.trivyignore`**: Add only documented exceptions with ADR references.

3. **Create `.trivy.yaml`**: Centralize Trivy configuration.

4. **Write exception review script**: Automated check for stale exceptions.

5. **Document exception process** in `docs/cve-exception-process.md`.

#### Verification Criteria

- [ ] `--ignore-unfixed=false` is explicitly set (already done)
- [ ] `.trivyignore` exists with documented exceptions only
- [ ] Each exception has a corresponding ADR or documented justification
- [ ] Exception review script runs in CI
- [ ] Trivy configuration is centralized in `.trivy.yaml`

---

### 3.8 T1.4.2: Create hermetic build environment (Dockerfile.ci)

#### Problem Analysis

Current CI installs tools ad-hoc in each step:

```yaml
- name: Install hadolint
  run: curl -sSfL ... -o /usr/local/bin/hadolint && chmod +x

- name: Install scanning tools
  run: curl ... | sh -s -- -b /usr/local/bin   # Trivy
       curl ... | sh -s -- -b /usr/local/bin   # Grype
```

Problems:

1. Tool versions change between runs (non-reproducible)
2. Download URLs could be compromised
3. No isolation between CI steps
4. Build environment not auditable

#### Solution: Pinned Hermetic CI Container

Create `Dockerfile.ci` that:

- Pins all tool versions
- Contains no secrets
- Has minimal attack surface
- Can be built and pushed as its own image

```dockerfile
FROM debian:bookworm-slim@sha256:abcd... AS ci-builder

ARG HADOLINT_VERSION=2.12.0
ARG TRIVY_VERSION=0.50.1
ARG GRYPE_VERSION=0.74.3
ARG SYFT_VERSION=0.100.0
ARG COSIGN_VERSION=2.2.3
ARG DIVE_VERSION=0.12.0

RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io \
    curl \
    git \
    jq \
    python3 \
    shellcheck \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSfL "https://github.com/hadolint/hadolint/releases/download/v${HADOLINT_VERSION}/hadolint-Linux-x86_64" \
    -o /usr/local/bin/hadolint && chmod +x /usr/local/bin/hadolint

RUN curl -sSfL https://raw.githubusercontent.com/aquasecurity/trivy/v${TRIVY_VERSION}/contrib/install.sh \
    | sh -s -- -b /usr/local/bin v${TRIVY_VERSION}

RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/v${GRYPE_VERSION}/install.sh \
    | sh -s -- -b /usr/local/bin v${GRYPE_VERSION}

RUN curl -sSfL https://raw.githubusercontent.com/anchore/syft/v${SYFT_VERSION}/install.sh \
    | sh -s -- -b /usr/local/bin v${SYFT_VERSION}

RUN curl -sSfL https://github.com/sigstore/cosign/releases/download/v${COSIGN_VERSION}/cosign-linux-amd64 \
    -o /usr/local/bin/cosign && chmod +x /usr/local/bin/cosign

RUN curl -sSfL https://github.com/wagoodman/dive/releases/download/v${DIVE_VERSION}/dive_0.12.0_linux_amd64.tar.gz \
    | tar -xzO dive > /usr/local/bin/dive && chmod +x /usr/local/bin/dive
```

#### CI Integration

Update `build.yml` to use the hermetic container:

```yaml
jobs:
  lint:
    container:
      image: ghcr.io/wyattau/evergreenimageregistry/ci:latest
    steps:
      - name: Run hadolint
        run: hadolint ...
      # No tool installation needed
```

#### Implementation Steps

1. **Create `Dockerfile.ci`**: Pin all tool versions with SHA256 digests.

2. **Create `Dockerfile.ci.CHECKSUMS`**: Verify all downloaded tools.

3. **Build and test locally**: Verify all tools work inside the container.

4. **Update `build.yml`**: Use `container:` directive for lint, verify, and sign-push jobs.

5. **Create CI image build workflow**: Separate workflow to build and push the CI image on changes to `Dockerfile.ci`.

#### Verification Criteria

- [ ] `Dockerfile.ci` exists with all tool versions pinned
- [ ] Every tool download has checksum verification
- [ ] CI pipeline uses the hermetic container (no ad-hoc tool installs)
- [ ] Tool versions are upgradeable via single ARG change
- [ ] CI image is itself built and pushed via CI

---

## 4. Quality Gates

### Gate QG-1.1: All Downloads Verified by SHA256

| Criterion                                         | Measurement                                 | Threshold    |
| ------------------------------------------------- | ------------------------------------------- | ------------ |
| Images with curl downloads having CHECKSUMS files | CHECKSUMS files / curl-download images      | 100%         |
| Dockerfiles with sha256sum verification           | Verified / curl-download images             | 100%         |
| Build failure on checksum mismatch                | Inject bad hash, verify build fails         | Always fails |
| Error message quality                             | Check for expected vs actual hash in output | Present      |

### Gate QG-1.2: Images Signed with Keyless Cosign

| Criterion                    | Measurement                        | Threshold             |
| ---------------------------- | ---------------------------------- | --------------------- |
| Signature present            | `cosign verify` succeeds           | 100% of pushed images |
| Certificate identity matches | Identity check passes              | 100%                  |
| Rekor transparency log entry | `rekor-cli search` finds entry     | 100%                  |
| No key-based fallback        | No `COSIGN_PRIVATE_KEY` references | 0 references          |

### Gate QG-1.3: SLSA v3 Provenance Generated

| Criterion                      | Measurement                                                | Threshold |
| ------------------------------ | ---------------------------------------------------------- | --------- |
| Provenance attestation present | `cosign verify-attestation` succeeds                       | 100%      |
| Source URI correct             | Source matches `github.com/WyattAu/EvergreenImageRegistry` | 100%      |
| `slsa-verifier` validation     | Verification passes                                        | 100%      |

### Gate QG-1.4: No Secrets in Any Dockerfile

| Criterion              | Measurement                  | Threshold |
| ---------------------- | ---------------------------- | --------- |
| TruffleHog scan clean  | Exit code 0                  | Always    |
| TruffleHog blocking    | `continue-on-error` is false | Always    |
| Pre-commit hook active | Hook runs on commit          | Confirmed |

### Gate QG-1.5: Trivy Scans All CVEs (No ignore-unfixed)

| Criterion                    | Measurement                     | Threshold |
| ---------------------------- | ------------------------------- | --------- |
| `--ignore-unfixed=false` set | Grep check                      | Present   |
| `.trivyignore` governance    | All entries have ADR references | 100%      |
| Exception expiry check       | Script runs and reports         | Active    |

---

## 5. Risk Register

| Risk                                                      | Probability | Impact   | Mitigation                                                           | Owner | Related Task |
| --------------------------------------------------------- | ----------- | -------- | -------------------------------------------------------------------- | ----- | ------------ |
| Upstream checksums unavailable for some binaries          | MEDIUM      | MEDIUM   | Compute from verified source, document in ADR                        | Nexus | T1.1.1       |
| Checksum verification breaks builds on legitimate updates | HIGH        | MEDIUM   | Automated checksum update script + clear documentation               | Nexus | T1.1.2       |
| Fulcio/Rekor OIDC token exchange fails                    | LOW         | HIGH     | Fallback to key-based signing with documented rotation procedure     | Nexus | T1.2.1       |
| TruffleHog false positives block legitimate builds        | MEDIUM      | MEDIUM   | `.trufflehogignore` with justification, per-file exclusions          | Nexus | T1.3.1       |
| Trivy finds unfixable CRITICAL CVEs in base images        | HIGH        | HIGH     | `.trivyignore` with ADR + compensating controls + base image refresh | Nexus | T1.4.1       |
| Hermetic CI container becomes stale                       | MEDIUM      | LOW      | Dependabot for `Dockerfile.ci` ARGs, monthly review                  | Nexus | T1.4.2       |
| GitHub OIDC issuer changes                                | LOW         | CRITICAL | Monitor Sigstore announcements, version-pin all actions              | Nexus | T1.2.1       |

---

## 6. Rollback Procedures

### If T1.1.1/T1.1.2 (checksum verification) causes widespread build failures:

1. Identify failing images and root cause (stale checksums, URL changes, etc.)
2. If upstream URL changed: update CHECKSUMS file and Dockerfile ARG
3. If upstream removed binary: file GitHub issue, temporarily revert to unchecked download with `# TODO: T1.1.2 pending`
4. If too many failures (>20%): revert checksum enforcement to warning-only mode, fix in batches

### If T1.2.1 (keyless Cosign) fails:

1. Revert to key-based signing with `COSIGN_PRIVATE_KEY` secret
2. Generate a new key pair with `cosign generate-key-pair`
3. Store public key as `cosign.pub` in repository root
4. Document the key rotation in an ADR

### If T1.3.1 (TruffleHog blocking) has false positives:

1. Add specific false positive to `.trufflehogignore`
2. Document the false positive with justification
3. Report upstream to TruffleHog if applicable
4. Set `continue-on-error: true` ONLY for the specific step, not globally

### If T1.4.2 (hermetic CI) breaks the pipeline:

1. Revert to ad-hoc tool installation
2. Debug Dockerfile.ci in isolation
3. Re-deploy after fixing

---

## 7. Success Metrics

| Metric                                | Current Value             | Target Value            | Measurement                                 |
| ------------------------------------- | ------------------------- | ----------------------- | ------------------------------------------- |
| Images with checksum verification     | 0 (0%)                    | 107 (100%)              | Grep for `sha256sum -c` in Dockerfiles      |
| Images signed with keyless Cosign     | 0 (0%)                    | 223 (100%)              | `cosign verify` against registry            |
| SLSA v3 provenance                    | 0 (0%)                    | 223 (100%)              | `slsa-verifier verify-image`                |
| SBOMs signed with keyless attestation | 0 (0%)                    | 223 (100%)              | `cosign verify-attestation --type spdxjson` |
| TruffleHog blocking                   | False (continue-on-error) | True                    | Check `build.yml`                           |
| Trivy ignore-unfixed                  | Already false             | Maintained              | Grep check                                  |
| `.trivyignore` governance             | Missing                   | All entries documented  | Manual review                               |
| Hermetic CI environment               | Missing                   | Active                  | Check `build.yml` container directive       |
| CVE exception process                 | Missing                   | Documented              | Check `docs/cve-exception-process.md`       |
| Supply chain attack surface           | HIGH (no verification)    | LOW (full verification) | Audit                                       |

---

**END OF PHASE 1 PLAN**
