# CI/CD Pipeline Guide

Authoritative reference for the Evergreen Image Registry CI/CD pipeline. This registry serves 1014+ container images
across four tiers for HFT (high-frequency trading) infrastructure.

---

## 1. Pipeline Architecture Overview

The pipeline is composed of four GitHub Actions workflow files:

| Workflow              | Trigger                       | Purpose                                    |
| --------------------- | ----------------------------- | ------------------------------------------ |
| `build-on-push.yml`   | Push to `main`, PRs to `main` | Incremental build of changed images        |
| `build-nightly.yml`   | Cron `0 3 * * *` (03:00 UTC)  | Full rebuild of all images                 |
| `build-on-demand.yml` | `workflow_dispatch`           | Manual builds with configurable parameters |
| `_build-reusable.yml` | Called by the three above     | Shared build, push, and sign logic         |

The build graph is manifest-driven. Each image under `images/<name>/` has a `manifest.toml` declaring its tier, version,
and build configuration. The top-level `manifest.toml` defines global settings (batch size, timeouts, tier defaults,
builder configuration).

Image discovery is handled by `scripts/discover-images.sh`, which supports four modes:

| Mode      | Argument                                            | Description                                   |
| --------- | --------------------------------------------------- | --------------------------------------------- |
| `changed` | (none)                                              | Images whose files changed in the last commit |
| `tier`    | `critical`, `standard`, `community`, `experimental` | All images in a tier                          |
| `images`  | Comma-separated names                               | Specific images by name                       |
| `all`     | (none)                                              | Every image with a Dockerfile                 |

The script outputs a JSON matrix consumed by GitHub Actions:

```json
{
  "include": [
    { "batch": 0, "images": "nginx,redis,grafana", "count": 3 },
    { "batch": 1, "images": "postgres,mysql", "count": 2 }
  ]
}
```

Batch size is controlled by `build.batch_size` in the top-level `manifest.toml` (default: 50). The matrix uses
`fail-fast: false` so one failing image does not abort the entire batch.

---

## 2. Tier System

Each image is assigned exactly one tier. The tier determines build schedule, signing policy, multi-arch support, and
push behavior.

### Tier Definitions

| Tier           | Count       | Schedule               | Sign | Multi-arch | Push         | SBOM |
| -------------- | ----------- | ---------------------- | ---- | ---------- | ------------ | ---- |
| `critical`     | 80          | Weekly (nightly in CI) | Yes  | Yes        | Always       | Yes  |
| `standard`     | 861         | Weekly (nightly in CI) | No   | Yes        | Nightly only | Yes  |
| `community`    | 71          | Monthly                | No   | No (amd64) | Nightly only | Yes  |
| `experimental` | Manual only | Manual                 | No   | No         | On demand    | No   |

### Tier Semantics

**Critical** -- Production services for internal HFT infrastructure. Zero failure tolerance. Every push touching a
critical image triggers an immediate build with signing and multi-arch output. Nightly rebuild is mandatory.

**Standard** -- Useful tools and services. Built on push when changed. Pushed during nightly builds. Failures are warned
but do not block other images.

**Community** -- Experimental or contributed images. Built on push when changed. amd64 only by default. Pushed during
nightly builds with warn-not-fail.

**Experimental** -- Unstable or work-in-progress. Manual dispatch only. No signing, no SBOM, no automatic pushes.

### Tier Assignment

Tier is declared per-image in `images/<name>/manifest.toml` under the `[metadata]` section:

```toml
[metadata]
name = "nginx"
version = "1.27.1"
tier = "critical"
```

There is no central list of images per tier. The tier for each image is resolved at build time by reading its manifest.

### Legacy Tier Mapping

Older manifests may use numeric tier values. The `resolve_tier()` function in `scripts/discover-images.sh` maps these to
semantic names:

```bash
"1" -> "critical"
"2" -> "standard"
"3" -> "community"
```

If a manifest has no `tier` field, the default is `"standard"`.

---

## 3. Build-on-Push Workflow

**File:** `.github/workflows/build-on-push.yml`

### Trigger

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'images/**'
      - 'scripts/**'
      - 'manifest.toml'
      - '.github/workflows/_build-reusable.yml'
      - '.github/workflows/build-on-push.yml'
  pull_request:
    branches: [main]
    paths:
      - 'images/**'
      - 'scripts/**'
      - 'manifest.toml'
```

### Behavior

1. **Discover** -- Runs `scripts/discover-images.sh changed` with `fetch-depth: 2` to compare against `HEAD~1`. If only
   shared infrastructure (scripts/, manifest.toml, CI workflows) changed but no specific image files, falls back to
   building critical tier only.
2. **Lint** -- Runs hadolint on changed Dockerfiles with `continue-on-error: true`. Failures are warnings, not gates.
3. **Build** -- Calls `_build-reusable.yml` with the discovered matrix.

### Push Policy

- Push to `main`: builds and pushes (push is enabled).
- Pull requests: builds only, does not push (`push: ${{ github.event_name != 'pull_request' }}`).
- Signing is always enabled for push-to-main builds.

### Concurrency

```yaml
concurrency:
  group: build-on-push-${{ github.ref }}
  cancel-in-progress: false
```

Concurrent pushes to the same ref are serialized. In-progress runs are not cancelled.

---

## 4. Build-Nightly Workflow

**File:** `.github/workflows/build-nightly.yml`

### Trigger

```yaml
on:
  schedule:
    - cron: '0 3 * * *'
  workflow_dispatch:
    inputs:
      tier:
        description: 'Build only this tier (leave empty for all)'
        type: choice
        options: ['', 'critical', 'standard', 'community']
      sign:
        description: 'Sign images with Cosign'
        type: boolean
        default: true
```

### Build Order

Images are built tier-by-tier in dependency order. Each tier is a separate job so failures in lower tiers do not block
higher tiers:

1. **Gates** -- Fast CI gate check verifying HEALTHCHECK and security labels on all Dockerfiles. Blocks all builds if it
   fails.
2. **Discover Critical / Standard / Community** -- Three parallel discover jobs produce independent matrices.
3. **Build Critical** -- Depends on gates and discover-critical. Pushes and signs all images.
4. **Build Standard** -- Depends on build-critical and discover-standard. Pushes but does not sign.
5. **Build Community** -- Depends on build-standard and discover-community. Pushes but does not sign. Multi-arch
   disabled (amd64 only).

### Report

The `report` job runs with `if: always()` and produces a markdown summary table with per-tier image counts and build
results:

```
| Tier      | Images | Build     |
|-----------|--------|-----------|
| Gates     | -      | success   |
| Critical  | 80     | success   |
| Standard  | 861    | success   |
| Community | 71     | failure   |
```

### Purpose

- Catch upstream version drift (base images, package versions).
- Verify all images still build against current toolchain.
- Detect dependency conflicts introduced by transitive updates.
- Validate multi-arch builds still work for critical and standard tiers.

---

## 5. Build-on-Demand Workflow (Manual Dispatch)

**File:** `.github/workflows/build-on-demand.yml`

### Inputs

| Input       | Type    | Default    | Description                              |
| ----------- | ------- | ---------- | ---------------------------------------- |
| `mode`      | choice  | (required) | `tier`, `images`, or `changed`           |
| `filter`    | string  | (empty)    | Tier name or comma-separated image names |
| `sign`      | boolean | `false`    | Sign images with Cosign                  |
| `multiarch` | boolean | `true`     | Build for amd64+arm64                    |
| `push`      | boolean | `true`     | Push to registry                         |
| `tag`       | string  | commit SHA | Custom tag override                      |

### Validation

The `validate` job checks inputs before proceeding:

- `tier` mode: filter must be `critical`, `standard`, `community`, or `experimental`.
- `images` mode: filter must be non-empty (comma-separated image names).
- `changed` mode: no filter required.

Invalid inputs produce an `::error::` annotation and fail the workflow.

### Use Cases

- **Test a single image:** mode=`images`, filter=`nginx`, push=`false`.
- **Rebuild failed batch:** mode=`images`, filter=`img1,img2,img3`, push=`true`.
- **Force-rebuild a tier after CVE fixes:** mode=`tier`, filter=`critical`.
- **Custom tag push:** mode=`images`, filter=`redis`, tag=`v7.4.8-patch1`.
- **Test CI changes without pushing to main:** mode=`changed` on a branch.

### Downstream Tier Label

The tier label passed to the reusable workflow is `demand-<mode>` (e.g., `demand-tier`, `demand-images`) for reporting
purposes.

---

## 6. Reusable Workflow (`_build-reusable.yml`) Design Decisions

**File:** `.github/workflows/_build-reusable.yml`

### Tarball-Load Push Pattern

Build and push are separate steps. The build step saves each image as a tarball via
`--output type=docker,dest=/tmp/images/<name>.tar`. The push step loads the tarball with `docker load -i <tarball>` and
pushes the loaded image.

This pattern exists to work around BuildKit COPY evaluation failures that occur when BuildKit re-evaluates Dockerfile
instructions during a push. By loading from a pre-built tarball, the push step bypasses BuildKit entirely.

Trade-off: The tarball contains a single-architecture image. Multi-arch pushes require a different strategy (buildx bake
with registry cache, not yet implemented).

```yaml
# Build step produces tarball
--output "type=docker,dest=/tmp/images/${SAFE}.tar"

# Push step loads tarball (no rebuild)
docker load -i "$TAR"
docker push "${REF}"
```

### Warn-Not-Fail Pattern

Individual image build failures emit `::warning::` annotations rather than failing the entire batch. This is critical
for nightly builds where one broken image should not prevent the other 1000+ images from being built and pushed.

```bash
if build_image "${image}"; then
    BUILT=$((BUILT+1))
else
    echo "::warning::${image}: build failed, retrying..."
    # ... retry once ...
    echo "::error::${image}: build failed after 2 attempts"
    FAILED=$((FAILED+1))
fi
```

Build failures trigger a single automatic retry with a 5-second delay. After two failures, the image is skipped and a
warning is emitted.

### always() Conditions

Push and sign steps use `if: always()` so they execute even when some matrix jobs fail:

```yaml
- name: Push to registry
  if: always() && inputs.push
  run: ...

- name: Sign Images
  needs: build
  if: always() && inputs.push && inputs.sign
  ...
```

This ensures that successfully built images are still pushed and signed even if other images in the same batch failed.

### Permissions

The reusable workflow declares `permissions: {}` at the top level. Per-job permissions are set on individual jobs. This
is a GitHub Actions requirement for reusable workflows -- the caller's permissions are not inherited unless explicitly
passed via `secrets: inherit`.

```yaml
permissions: {} # required: reusable workflows don't inherit caller permissions

jobs:
  build:
    permissions:
      contents: read
      packages: write
  sign:
    permissions:
      id-token: write
      packages: write
      contents: read
```

### Matrix Strategy

```yaml
strategy:
  fail-fast: false
  max-parallel: 5
  matrix: ${{ fromJson(inputs.matrix) }}
```

`fail-fast: false` is essential -- with 1014+ images, a single flaky build must not abort the entire run.
`max-parallel: 5` limits concurrent batch jobs to stay within GitHub Actions runner quotas.

### BuildKit Builder Lifecycle

The builder is recreated every 5 images to prevent BuildKit resource exhaustion:

```bash
if [ $((BUILT + FAILED)) -gt 0 ] && [ $(( (BUILT + FAILED) % 5 )) -eq 0 ]; then
    recreate_builder
fi
```

Builder configuration uses BuildKit v0.12.0 with unlimited log size:

```yaml
driver-opts: |
  image=moby/buildkit:v0.12.0
  env.BUILDKIT_STEP_LOG_MAX_SIZE=-1
  env.BUILDKIT_STEP_LOG_MAX_SPEED=10
```

### Artifact Upload

Build tarballs and image reference lists are uploaded as artifacts with 7-day retention:

```yaml
- name: Upload image tarballs
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: images-${{ inputs.tier }}-batch-${{ matrix.batch }}
    path: /tmp/images/
    retention-days: 7

- name: Upload built image references
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: built-list-${{ inputs.tier }}-batch-${{ matrix.batch }}
    path: /tmp/built-images.txt
    retention-days: 7
```

These artifacts are consumed by the sign job and are available for debugging failed builds.

---

## 7. Build Step Internals

### Docker Build Command

```bash
docker buildx build \
    --builder "$CURRENT_BUILDER" \
    --platform linux/amd64 \
    -t "${REF}" \
    --output "type=docker,dest=/tmp/images/${SAFE}.tar" \
    --no-cache \
    --build-arg "BUILD_DATE=${TAG}" \
    --build-arg "VCS_REF=${TAG}" \
    --build-arg "TARGETARCH=amd64" \
    --build-arg "GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}" \
    --label "org.opencontainers.image.source=${{ github.server_url }}/${{ github.repository }}" \
    --label "org.opencontainers.image.revision=${{ github.sha }}" \
    "./images/${image}"
```

Key flags:

- `--no-cache` -- Ensures fully clean builds for reproducibility. Nightly rebuilds must not be affected by stale cache
  layers.
- `--output type=docker,dest=...` -- Produces a tarball instead of loading into local Docker daemon.
- `--build-arg GITHUB_TOKEN` -- Passed for same-repo file downloads only (e.g., `COPY` from the same repository). Must
  not be used for cross-repo downloads (see Section 10).
- `--label org.opencontainers.image.source` / `revision` -- OCI standard labels for traceability.

### Build Arguments

| Argument       | Source                 | Purpose                                                 |
| -------------- | ---------------------- | ------------------------------------------------------- |
| `BUILD_DATE`   | Tag value              | Build timestamp for OCI labels                          |
| `VCS_REF`      | Tag value              | Git reference for OCI labels                            |
| `TARGETARCH`   | Always `amd64`         | Target architecture for `ARG TARGETARCH` in Dockerfiles |
| `GITHUB_TOKEN` | `secrets.GITHUB_TOKEN` | Auth for same-repo downloads                            |

### Reproducibility

`SOURCE_DATE_EPOCH` is set from the current timestamp at the start of each job:

```yaml
- name: Set SOURCE_DATE_EPOCH
  run: echo "SOURCE_DATE_EPOCH=$(date -u +%s)" >> "$GITHUB_ENV"
```

This ensures consistent timestamps across layers for reproducible builds.

### Multi-Architecture

Multi-arch is controlled at two levels:

1. **Workflow level:** The `multiarch` input to `_build-reusable.yml` (set by the calling workflow based on tier).
2. **Per-image level:** The `multiarch` field in `images/<name>/manifest.toml`.

Images that should not build multi-arch include Go source builds (QEMU emulation timeout), Rust source builds, and
images with architecture-specific dependencies. For these images, set `multiarch = false` in the per-image manifest.

Currently, the build step always produces `linux/amd64` tarballs. Multi-arch support via buildx bake is a planned
improvement (see Section 12).

### Timeouts

| Timeout         | Value                 | Scope                                          |
| --------------- | --------------------- | ---------------------------------------------- |
| Per-image build | 900 seconds (15 min)  | `timeout` wrapper around `docker buildx build` |
| Per-image push  | 300 seconds (5 min)   | `timeout` wrapper around `docker push`         |
| Batch job       | 360 minutes (6 hours) | `timeout-minutes` on the job                   |
| Sign job        | 30 minutes            | `timeout-minutes` on the sign job              |

### Image Size Enforcement

After building, an enforcement step checks tarball sizes against limits defined in `manifest.toml`:

```toml
[build.size_limit]
scratch_mb = 50
distroless_mb = 50
wolfi_mb = 200
debian_slim_mb = 200
```

Exceeding the limit emits an `::error::` annotation. The check uses `continue-on-error: true` so it warns without
blocking.

### Build Cache

The top-level manifest declares GHA cache configuration:

```toml
[build.cache]
type = "gha"
mode = "max"
compression = "zstd"
```

Note: The current build step uses `--no-cache`, so cache is not actively used during builds. This configuration is
reserved for future use when selective caching is enabled.

---

## 8. Push and Sign Step Internals

### Push

The push step iterates over the same image list from the matrix. For each image:

1. Check if the tarball exists at `/tmp/images/<name>.tar`.
2. Load the tarball: `docker load -i "$TAR"`.
3. Tag the image: `docker tag "${REF}" "${REF}"`.
4. Push: `docker push "${REF}"`.
5. Sleep 2 seconds between pushes to avoid rate limiting.

If a tarball is missing (build failed), the push is skipped with a warning:

```bash
if [ -f "$TAR" ]; then
    docker load -i "$TAR" 2>/dev/null || true
    docker push "${REF}" 2>&1
else
    echo "::warning::${image}: no tarball (build failed), skipping push"
fi
```

### Registry

Primary registry: `ghcr.io/<owner>/<image-name>`

Docker Hub login is attempted with `continue-on-error: true`:

```yaml
- name: Login to Docker Hub
  if: inputs.push
  continue-on-error: true
  uses: docker/login-action@v3
  with:
    registry: docker.io
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

Docker Hub publication is not yet fully implemented. The login is present for future use.

### Tags

Each image receives a single tag per build. The tag is determined by the calling workflow:

- **Push to main:** `${{ github.sha }}` (full commit SHA).
- **Nightly:** `${{ github.sha }}`.
- **On-demand:** Custom tag from `inputs.tag`, or `${{ github.sha }}` if not specified.

Additional tags (`:version`, `:latest`, `:sha-<short>`) are planned for future implementation.

### Sign

Signing uses Cosign keyless signing via Fulcio OIDC:

```bash
cosign sign --yes \
    --certificate-identity="${{ github.repository_owner }}" \
    --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
    "${ref}"
```

The sign job downloads all `built-list-*` artifacts from the build job, concatenates the image reference lists, and
signs each unique reference. Sign failures emit `::warning::` and do not block the workflow.

Signing requires `id-token: write` permission for OIDC token generation.

---

## 9. manifest.toml Per-Image Configuration

### Top-Level Manifest (`manifest.toml` at repo root)

Defines global build settings and tier defaults:

```toml
[registry]
name = "ghcr.io/wyattau/evergreenimageregistry"
default_platforms = ["linux/amd64", "linux/arm64"]

[build]
batch_size = 50
per_image_timeout_seconds = 900
batch_timeout_minutes = 360
max_parallel_batches = 5
builder_recreate_interval = 5
builder_image = "moby/buildkit:v0.12.0"

[tier.critical]
description = "Production images for internal HFT infrastructure"
sign = true
sbom = true
multiarch = true

[tier.standard]
description = "Community and multi-company images"
sign = false
sbom = true
multiarch = true

[tier.community]
description = "Contributed images, lower priority"
sign = false
sbom = true
multiarch = false
```

### Per-Image Manifest (`images/<name>/manifest.toml`)

```toml
[metadata]
name = "nginx"
version = "1.27.1"
description = "Nginx - HTTP and reverse proxy server"
vendor = "Nginx Inc"
source = "https://github.com/nginx/nginx"
license = "BSD-2-Clause"
tier = "critical"
upstream_version = "1.27.1"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "package-manager"
url = "https://github.com/nginx/nginx/releases/download/v1.27.1/nginx-1.27.1-linux-amd64.tar.gz"

[runtime]
entrypoint = ["/nginx"]

[ports]
expose = [80, 443, 9101]

[labels]
"org.opencontainers.image.title" = "nginx"
"evergreen.image.tier" = "critical"
"evergreen.hft.deploy-strategy" = "hft-rolling"
```

### Field Reference

| Field              | Section      | Required | Description                                                                    |
| ------------------ | ------------ | -------- | ------------------------------------------------------------------------------ |
| `name`             | `[metadata]` | Yes      | Image name (must match directory name)                                         |
| `version`          | `[metadata]` | Yes      | Semantic version                                                               |
| `tier`             | `[metadata]` | No       | `critical`, `standard`, `community`, or `experimental`. Defaults to `standard` |
| `description`      | `[metadata]` | No       | Human-readable description                                                     |
| `vendor`           | `[metadata]` | No       | Upstream vendor name                                                           |
| `source`           | `[metadata]` | No       | Upstream source URL                                                            |
| `license`          | `[metadata]` | No       | SPDX license identifier                                                        |
| `upstream_version` | `[metadata]` | No       | Exact upstream version for version tracking                                    |
| `base`             | `[build]`    | No       | Base image reference                                                           |
| `user`             | `[build]`    | No       | UID:GID for the runtime user                                                   |
| `stopsignal`       | `[build]`    | No       | Container stop signal                                                          |
| `entrypoint`       | `[runtime]`  | No       | Container entrypoint                                                           |
| `cmd`              | `[runtime]`  | No       | Container default command                                                      |
| `expose`           | `[ports]`    | No       | List of exposed ports                                                          |
| `multiarch`        | `[build]`    | No       | Override multi-arch for this image                                             |

### Multi-Arch Overrides

Set `multiarch = false` in the `[build]` section of a per-image manifest to disable multi-arch builds for that specific
image. Use this for:

- Go source builds that timeout under QEMU emulation.
- Rust source builds with architecture-specific compilation.
- Images with dependencies only available for amd64.

---

## 10. Common CI Failures and Remedies

### BuildKit COPY Evaluation Failure

**Error:** `failed to calculate checksum of ref::<sha>:: failed to walk ...`

**Cause:** BuildKit re-evaluates `COPY` instructions during push, which can fail when the build context has changed or
when using multi-stage builds with complex COPY patterns.

**Remedy:** The tarball-load push pattern in `_build-reusable.yml` already handles this. The build step saves a tarball,
and the push step loads it with `docker load` instead of rebuilding.

**Reference:** `dockerfile-standards.md` Section 2.

### GITHUB_TOKEN 404 on Cross-Repo Downloads

**Error:** `404 Not Found` when a Dockerfile uses `COPY` or `ADD` to download from a different repository.

**Cause:** `GITHUB_TOKEN` only has access to the current repository. Cross-repo downloads fail with 404.

**Remedy:** Remove authentication headers for cross-repo URLs. Use public URLs without passing `GITHUB_TOKEN` as a build
argument for those specific downloads.

**Reference:** `dockerfile-standards.md` Section 5.

### wolfi Base Image: curl Not Found

**Error:** `/bin/sh: curl: not found` in Dockerfiles based on wolfi/Chainguard.

**Cause:** wolfi minimal images do not include curl by default.

**Remedy:** Use `wget` instead of `curl` in Dockerfiles.

**Reference:** `dockerfile-standards.md` Section 4.

### Push Rebuild Failures

**Error:** Push step fails because BuildKit attempts to rebuild the image.

**Remedy:** Already handled by the tarball-load pattern. The push step calls `docker load -i <tarball>` and never
invokes BuildKit.

### Matrix Timeout

**Error:** Batch job exceeds 6-hour timeout.

**Cause:** Too many slow-building images in a single batch.

**Remedy:** Reduce `build.batch_size` in `manifest.toml`. Check per-image build times in the Actions log. Images
exceeding 15 minutes should be investigated for optimization (smaller base, fewer layers, pre-built binaries).

### Rate Limiting

GitHub API: 5,000 requests/hour per token. GitHub Packages: 100 GB bandwidth per month on free tier.

**Symptoms:** `docker push` returns 429, or API calls in scripts fail with 403.

**Remedies:**

- The 2-second sleep between pushes in the push step mitigates burst rate limiting.
- Monitor bandwidth usage in GitHub repository settings.
- For high-volume operations, use a PAT with higher rate limits stored as a repository secret.

### BuildKit Builder Exhaustion

**Symptoms:** Builds hang or fail with `no space left on device` or OOM.

**Remedy:** The builder is automatically recreated every 5 images (`builder_recreate_interval = 5`). If exhaustion
occurs more frequently, reduce this value in `manifest.toml`.

---

## 11. Monitoring and Alerts

### Actions Dashboard

All build runs are visible at: `https://github.com/WyattAu/EvergreenImageRegistry/actions`

### Annotations

- `::error::` -- Hard failures that fail the step (e.g., validation errors, image size violations).
- `::warning::` -- Soft failures that do not block the workflow (e.g., build failures for individual images in nightly
  builds).
- `::notice::` -- Informational messages (e.g., "no images changed", builder recreation).

Annotations are visible in the Actions log for each workflow run and in PR checks.

### Nightly Report

The nightly workflow generates a markdown summary table posted to the Actions run summary page. It includes:

- Gate check result (pass/fail).
- Per-tier image count and build result (success/failure/skipped).
- Commit SHA that triggered the build.

### Critical Tier Failure Response

Critical tier has zero failure tolerance. If `build-critical` fails in the nightly build:

1. The report shows `failure` for the critical row.
2. Individual failed images are listed in the `::error::` annotations.
3. Investigation is required before the next trading day.

### Build Monitor Script

`scripts/build_monitor.py` provides programmatic access to build results for custom alerting integrations.

---

## 12. Future Improvements

### Multi-Arch Push via buildx Bake

Replace the tarball-load pattern with `docker buildx bake` for multi-arch pushes. This would eliminate the single-arch
limitation of tarballs and enable native multi-platform manifest creation.

### Docker Hub Mirror Publication

The Docker Hub login is already present in `_build-reusable.yml`. Full mirror publication requires adding Docker Hub
tagging and push logic alongside the ghcr.io push.

### SBOM Generation per Image

SBOM generation scripts already exist (`scripts/generate_sbom.sh`, `scripts/generate_all_sboms.sh`). Integration into
the CI pipeline as a post-build step would produce SBOMs for every image and attach them as workflow artifacts.

### CVE Scanning Gate

Block push of images with critical or high CVEs. This would use Trivy or Grype (both already available as images in the
registry) as a scanning step between build and push.

### Digest Pinning Automation

`scripts/pin_digests.sh` exists for pinning image digests. Integration into the CI pipeline would automatically update
`FROM` lines to pinned digests after successful builds.

### Image Promotion Pipeline

Automated promotion path: `community` -> `standard` -> `critical`. This would require:

1. Automated quality gates (build success rate, CVE scan, SBOM completeness).
2. A promotion workflow that updates the `tier` field in per-image manifests.
3. Review/approval step for critical tier promotion.
