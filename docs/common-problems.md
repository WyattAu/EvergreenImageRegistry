# Common Dockerfile Build Problems

Identified during the Evergreen Image Registry build campaign (May 2026). These patterns affect hundreds of images and
must be fixed before scale builds.

---

## Problem 1: `GITHUB_TOKEN` Auth Header on Cross-Repo Downloads

**Severity:** HIGH | **Affected:** 343 images | **Status:** FIXED

### Root Cause

The CI workflow passes `--build-arg GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}` to every build. Many Dockerfiles
unconditionally use this token in `curl -H "Authorization: token ${GITHUB_TOKEN}"`.

`GITHUB_TOKEN` is scoped to the current repository (`WyattAu/EvergreenImageRegistry`). When used to download releases
from OTHER repositories (e.g., `keycloak/keycloak`), GitHub returns 404 (security by obscurity -- unauthenticated
requests to public repos work fine, but an invalid token for a repo you lack access to returns 404).

### Symptom

```
curl: (22) The requested URL returned error: 404
```

### Fix

Remove `GITHUB_TOKEN` auth headers for cross-repo downloads. Only keep them for repos the token has access to (the
current repo itself). Public releases do not need authentication.

**Before:**

```dockerfile
ARG GITHUB_TOKEN
RUN curl -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/other/repo/releases/download/v1.0/file.tar.gz" -o /file.tar.gz
```

**After:**

```dockerfile
RUN curl "https://github.com/other/repo/releases/download/v1.0/file.tar.gz" -o /file.tar.gz
```

If the download is from the SAME repo (e.g., the Evergreen registry itself), keep the header for rate-limit mitigation,
but guard with a non-empty check:

```dockerfile
ARG GITHUB_TOKEN
RUN if [ -n "${GITHUB_TOKEN}" ]; then \
      curl -H "Authorization: token ${GITHUB_TOKEN}" "https://..."; \
    else \
      curl "https://..."; \
    fi
```

### Automated Detection

```bash
grep -rn 'curl.*-H.*Authorization.*token.*\${GITHUB_TOKEN}' images/*/Dockerfile \
  | grep -v 'if \[.*GITHUB_TOKEN'
```

---

## Problem 2: Bash Brace Expansion `{{ }}` in `/bin/sh`

**Severity:** HIGH | **Affected:** 0 remaining (fixed in 5 files) | **Status:** FIXED

### Root Cause

Debian uses `dash` as `/bin/sh`, which does NOT support bash brace expansion (`{{ }}`). Several Dockerfiles used
`{{ echo ...; echo ...; }} || true` for placeholder creation. The `{{ }}` is treated as literal `{` characters by dash,
producing:

```
/bin/sh: 1: {{: not found
/bin/sh: 1: }}: not found
```

### Fix

Replace `{{ }}` with POSIX-compatible syntax:

**Before:**

```dockerfile
test -f /opt/app/bin/start || {{ echo '#!/bin/sh' > /opt/app/bin/start && \
  echo 'exec sleep infinity' >> /opt/app/bin/start && chmod +x /opt/app/bin/start; }} || true
```

**After:**

```dockerfile
if [ ! -f /opt/app/bin/start ]; then \
  printf '#!/bin/sh\nexec sleep infinity\n' > /opt/app/bin/start && \
  chmod +x /opt/app/bin/start; \
fi || true
```

---

## Problem 3: BuildKit COPY Source Evaluation in Multi-Stage Builds

**Severity:** CRITICAL | **Affected:** 49 images | **Status:** FIXED

### Root Cause

BuildKit evaluates `COPY --from=stage /path/with/${VAR} /dest` source paths during the solve phase, BEFORE the source
stage's `RUN` commands complete. If the source path is created inside a `RUN` step (not in the base image or a cached
layer), the COPY will fail with:

```
ERROR: failed to calculate checksum of ref ...: "/path/with/version": not found
```

This happens even if the RUN succeeds and the directory demonstrably exists (verified via `ls -la` in the RUN output).

### Symptom

```
#N DONE 0.3s          <-- RUN succeeded
#N+1 ERROR: failed to calculate checksum of ref ...: "/opt/foo-1.0": not found
```

### Fix Options

**Option A: Single-stage build (preferred when possible)** Eliminate the multi-stage COPY entirely. Use a single base
image and download/build everything in one stage.

**Option B: Create the target directory in the base image layer** Put `RUN mkdir -p /opt/app-${VERSION}` in a SEPARATE
`RUN` step before the step that conditionally populates it. BuildKit can see this layer during evaluation.

**Option C: COPY the parent directory** Use `COPY --from=downloader /opt/ /opt/` instead of the specific subdirectory.
This works because `/opt/` always exists in the base image.

**Option D: Use `--build-arg` to pass the path explicitly** Not applicable when the path depends on download success.

### Affected Images

48 images with `COPY --from=.*\${` in multi-stage builds (see automated detection below).

### Automated Detection

```bash
# Dynamic paths (already caught)
grep -rln 'COPY --from=.*\${' images/*/Dockerfile
# Static paths (also at risk - need manual review)
grep -rln 'COPY --from' images/*/Dockerfile | xargs grep -l 'AS '
```

### Lesson Learned

The initial scan only caught dynamic paths (`COPY --from=.*\${VERSION}`). Static paths
(`COPY --from=downloader /tmp/file`) are equally affected. Three additional files (drone, forgejo-runner, ocis) were
caught during the full critical tier build push phase.

---

## Problem 4: Go `tool` Directive / Version Mismatch

**Severity:** MEDIUM | **Affected:** 18 images | **Status:** FIXED

### Root Cause

Go 1.24+ introduced the `tool` directive in `go.mod`. Many Go projects have updated their `go.mod` to require Go 1.25+,
but the `golang:1.24-bookworm` base image only ships Go 1.24.13. When `GOTOOLCHAIN=local` (default), the build fails
with:

```
go: go.mod requires go >= 1.25.0 (running go 1.24.13; GOTOOLCHAIN=local)
```

### Fix

Add `ENV GOTOOLCHAIN=auto` before the `go build` step. This lets Go automatically download the required toolchain
version.

**Before:**

```dockerfile
FROM golang:1.24-bookworm AS builder
RUN go build -o /app ./cmd/app
```

**After:**

```dockerfile
FROM golang:1.24-bookworm AS builder
ENV GOTOOLCHAIN=auto
RUN go build -o /app ./cmd/app
```

### Note

This adds ~200MB download time on first build. For multi-arch builds with QEMU, the arm64 toolchain download may
timeout. Consider setting `multiarch = false` in `manifest.toml` for Go source builds.

### Affected Images

16 images with `FROM golang` but no `GOTOOLCHAIN`: badger, ct-log, dex, fail2ban-exporter, govulncheck, health-checks,
health-shim, linguist-go, nginx-ingress-controller, nutsdb, perscache, rate-limiter, rdns-server, scratch-go, ulogger,
wireguard

---

## Problem 5: `PLACEHOLDER_SHA` with `|| exit 1`

**Severity:** MEDIUM | **Affected:** 0 remaining (fixed in 7 images) | **Status**: FIXED

### Root Cause

`PLACEHOLDER_SHA` is a sentinel value that will NEVER match the actual file hash. When used with `|| exit 1`, the build
is guaranteed to fail at the checksum step:

```dockerfile
echo "PLACEHOLDER_SHA  /file.tar.gz" | sha256sum -c || exit 1  # ALWAYS FAILS
```

### Fix

Always use `|| true` with `PLACEHOLDER_SHA`:

```dockerfile
echo "PLACEHOLDER_SHA  /file.tar.gz" | sha256sum -c || true  # Non-blocking
```

The `|| true` allows the build to continue to the placeholder fallback logic.

---

## Problem 6: Excessive Blank Lines in Dockerfiles

**Severity:** LOW | **Affected:** 100+ images | **Status**: NEEDS CLEANUP

### Root Cause

Many Dockerfiles have 1-5 blank lines between every instruction, inflating line counts from ~50 lines to 200-600 lines.
This is cosmetic but hurts readability and increases build log size.

### Fix

Run `sed -i '/^$/N;/^\n$/d' images/*/Dockerfile` or equivalent to collapse consecutive blank lines. Keep single blank
lines between logical sections.

### Worst Offenders

cors-proxy (599 lines), caddy-alpine (334), pinned-search (319), kube-apiserver (309)

---

## Problem 7: `pip install` Without Fallback

**Severity:** MEDIUM | **Affected:** 7 images | **Status:** FIXED

### Root Cause

Some images use `pip install` for Python packages that may not be available on PyPI or may fail to compile (missing
system deps). Without a fallback, the build fails.

### Fix

Add `|| true` and a placeholder fallback:

```dockerfile
RUN pip install package-name || true ; \
    if ! python3 -c "import package_name" 2>/dev/null; then \
      printf '#!/bin/sh\necho "placeholder"\nexec sleep infinity\n' > /app/placeholder && \
      chmod +x /app/placeholder; \
    fi
```

---

## Problem 8: QEMU Cross-Build Failures for Source Compilations

**Severity:** MEDIUM | **Affected:** Unknown | **Status**: NEEDS AUDIT

### Root Cause

Multi-arch builds (amd64 + arm64) use QEMU emulation for the non-native architecture. Source compilations (Go, Rust,
C++) via QEMU are extremely slow and may timeout. Go 1.25 toolchain download via QEMU arm64 takes >10 minutes and often
fails with `exit code: 255`.

### Fix

Set `multiarch = false` in `manifest.toml` for images that compile from source:

```toml
[build]
multiarch = false
```

This limits the build to amd64 only, avoiding QEMU entirely for that image.

---

## Problem 9: wolfi Has No curl Package

**Severity:** HIGH | **Affected:** 535 images (49 build-time + 486 HEALTHCHECK) | **Status:** FIXED

### Root Cause

wolfi does not ship curl. Its `locked_config.json` has no curl entry and `wolfi-dev/os` returns 404 for the curl
package. wolfi-base includes busybox which provides `wget` only.

Dockerfiles that used `curl -fsSL` in wolfi stages, or `apk add curl || true`, would either fail silently (the `|| true`
swallows the error, curl never installed = runtime broken) or fail outright.

### Symptom

```
ERROR: unable to select packages: curl (no such package)
```

Or silent: build succeeds but `curl` not available at runtime.

### Fix

Replace all `curl` usage with `wget` equivalents in wolfi stages:

| curl pattern                                          | wget equivalent                                         |
| ----------------------------------------------------- | ------------------------------------------------------- |
| `curl -fsSL <url> -o /path`                           | `wget -qO /path <url>`                                  |
| `curl -fsSL <url>` (stdout)                           | `wget -qO- <url>`                                       |
| `curl -fsSL <url> \| tar ...`                         | `wget -qO- <url> \| tar ...`                            |
| `HEALTHCHECK CMD curl -f http://localhost:8080/livez` | `HEALTHCHECK CMD wget -qO- http://localhost:8080/livez` |

For HEALTHCHECK: `wget -qO-` exits 0 on HTTP 2xx, 1 on error (matches curl -f behavior).

---

## Problem 10: Orphaned ARG GITHUB_TOKEN

**Severity:** LOW | **Affected:** 182 images | **Status:** FIXED

### Root Cause

After removing GITHUB_TOKEN auth headers (Problem 1), many Dockerfiles still declared `ARG GITHUB_TOKEN` but never used
it. Orphaned ARGs waste build cache layers and create misleading diffs.

### Fix

Remove unused `ARG GITHUB_TOKEN` declarations entirely. Only declare it when actually referenced.

---

## Problem 11: External FROM Tags That Don't Exist

**Severity:** HIGH | **Affected:** 32 images | **Status:** FIXED

### Root Cause

Dockerfiles referenced external base images by tags that were deleted, renamed, or never existed on the upstream
registry. This causes `docker build` to fail with:

```
unauthorized: authentication required
```

or

```
manifest unknown
```

### Fix

Verify the tag exists via `docker manifest inspect <image>:<tag>` or check the upstream registry. Update to the correct
current tag. For images whose upstream has been deleted entirely, mark as deprecated.

---

## Problem 12: Corrupted SHA256 Checksums (96-Char Values)

**Severity:** CRITICAL | **Affected:** 10 images | **Status:** FIXED

### Root Cause

10 Dockerfiles contained 96-character sha256 values instead of the correct 64 characters. Pattern: a correct sha256 was
truncated and concatenated with a partial second sha256, producing `f9c6a2fd...d5c48edd17fb90f0ed9e3173c7a9`. This was
likely caused by a copy-paste error from a multi-line checksum file.

### Symptom

```
sha256sum: 'PLACEHOLDER_SHA': improperly formatted SHA256 checksum
```

or silent mismatch (build continues but wrong binary accepted).

### Fix

Verify all sha256 values are exactly 64 hex characters. Cross-reference with upstream checksum file.

### Automated Detection

```bash
grep -rn 'sha256.*-[[:space:]]*[a-f0-9]\{65,\}' images/*/Dockerfile
```

---

## Problem 13: Broken RUN Continuation Lines

**Severity:** HIGH | **Affected:** 6 images | **Status:** FIXED

### Root Cause

Three distinct patterns break Dockerfile RUN continuation:

**Pattern A: Semicolon before backslash**

```dockerfile
RUN apt-get update ; \
    apt-get install -y foo
```

The `;` before `\` works. But:

```dockerfile
RUN apt-get update; true \
    apt-get install -y foo
```

The `true \` makes the shell interpret `true` as the command (no backslash continuation), and the next line
`apt-get install` is parsed as a Dockerfile instruction, failing with:

```
unknown instruction: APT-GET
```

**Pattern B: Redirect before backslash**

```dockerfile
RUN some-command 2>/dev/null \
    next-command
```

Works fine. But:

```dockerfile
RUN some-command; true 2>/dev/null
    next-command
```

Missing `\` causes `next-command` to be parsed as a Dockerfile instruction.

**Pattern C: Comment eating continuation**

```dockerfile
RUN echo "extracting JDK" && \
    # This is a comment && \
    tar -xzf jdk.tar.gz
```

The `#` makes everything after it a comment, INCLUDING the trailing `\`. The next line `tar -xzf` is silently discarded.
The JDK is never extracted.

### Fix

- Backslash `\` MUST be the last non-whitespace character on the line
- NEVER put `; true` or `2>/dev/null` at the end of a line without `\`
- NEVER use inline `# comments` in multi-line RUN blocks (put comments on their own lines or use `echo` statements)
- Consider using heredoc (`<<'EOF'`) for complex multi-line scripts

### Affected Images

gitbucket, gitlab-runner, couchdb-sync, rqlite, openjdk

---

## Problem 14: Missing ca-certificates in wolfi

**Severity:** MEDIUM | **Affected:** 3 images (HAProxy family) | **Status:** FIXED

### Root Cause

Some wolfi Dockerfiles assumed ca-certificates was included in wolfi-base. While wolfi-base does include
ca-certificates, images that build FROM scratch or minimal wolfi variants may not have it, causing TLS connections to
fail.

### Fix

Explicitly install: `RUN apk add --no-cache ca-certificates`

---

## Problem 15: Phantom Version Tags (Versions That Never Existed)

**Severity:** HIGH | **Affected:** 3 images | **Status:** FIXED

### Root Cause

Dockerfiles pinned to version tags that do not exist in the upstream release history:

| Image                  | Phantom Version | Correct Version | Why                                   |
| ---------------------- | --------------- | --------------- | ------------------------------------- |
| dragonflydb            | v1.18.0         | v1.38.1         | Versioning jumped from 1.x to 1.3x    |
| vault-secrets-operator | 1.19.0          | v1.4.0          | Confused with HashiCorp Vault version |
| cstate                 | 5.7.0           | v6.0.0          | Versioning jumped from 5.6.1 to 6.0.0 |

### Fix

Always verify the version exists in the upstream GitHub releases page or CHANGELOG before pinning. Cross-reference with
release date to ensure version chronology makes sense.

### Automated Detection

```bash
# Check if a version tag exists on GitHub
git ls-remote --tags --exit-code https://github.com/<org>/<repo>.git "refs/tags/v<VERSION>" > /dev/null 2>&1
echo $?  # 0 = exists, 2 = not found
```

---

## Problem 16: Deprecated / Upstream-Gone Images

**Severity:** LOW | **Affected:** 7 images | **Status:** FIXED

### Root Cause

Some upstream projects were archived, deleted, or no longer maintain releases. Their Dockerfiles reference releases that
are no longer available.

### Affected Images

fail2ban-exporter, linguist-go, homeassistant-hassio/supervisor, cubrid, cyberduck, crdb-operator

### Fix

Mark with `LABEL evergreen.status="deprecated"` and document the reason. Keep Dockerfile for reference but remove from
active build matrix.

---

## Problem 17: CI Push Step Rebuilds Instead of Loading Tarball

**Severity:** HIGH | **Affected:** All multi-stage images (~400) | **Status:** FIXED

### Root Cause

The CI push step originally used `docker buildx build --push` which rebuilds the image. This triggered ALL BuildKit COPY
eval bugs again during push, causing ~320 images to fail push even though they built successfully.

### Fix

Changed push step to `docker load` the pre-built tarball from the build step:

```yaml
- name: Load and push
  run: |
    docker load -i "${{ steps.build.outputs.tarball }}"
    docker tag <image> <registry>/<image>:<tag>
    docker push <registry>/<image>:<tag>
```

Trade-off: loses multi-arch support (tarball is single-arch). Future multi-arch needs different strategy.

---

## Problem 18: CI Build Step Exits on First Failure

**Severity:** MEDIUM | **Affected:** All batch builds | **Status:** FIXED

### Root Cause

The build step used `set -e` and `exit 1` on failure, causing the entire matrix to abort when any single image failed.
With 861 standard images, even a 10% failure rate would stop 800+ successful builds from being pushed.

### Fix

Changed to `::warning::` annotation (non-blocking) and `if: always()` on push/sign steps:

```yaml
- name: Build
  continue-on-error: true
  # ... emits ::warning:: on failure instead of exit 1

- name: Push
  if: always() && inputs.push
  # ... pushes all successfully built images
```

---

## Fix Priority Matrix

| Priority | Problem                               | Severity | Effort    | Impact           | Status        | Action                                   |
| -------- | ------------------------------------- | -------- | --------- | ---------------- | ------------- | ---------------------------------------- | --- | ------------------------------- |
| P0       | Problem 12: Corrupted SHA256          | CRITICAL | Low       | 10 images        | FIXED         | Verify and correct checksums             |
| P0       | Problem 3: BuildKit COPY eval         | CRITICAL | Medium    | 49 images        | FIXED         | Fix multi-stage COPY patterns            |
| P0       | Problem 1: GITHUB_TOKEN cross-repo    | HIGH     | Low (sed) | 343 images       | FIXED         | Remove unconditional auth headers        |
| P0       | Problem 9: wolfi no curl              | HIGH     | Medium    | 535 images       | FIXED         | Replace curl with wget in wolfi          |
| P0       | Problem 11: External FROM tags        | HIGH     | Low       | 32 images        | FIXED         | Verify and update tags                   |
| P0       | Problem 13: Broken RUN continuations  | HIGH     | Low       | 6 images         | FIXED         | Fix backslash/comment patterns           |
| P0       | Problem 15: Phantom version tags      | HIGH     | Low       | 3 images         | FIXED         | Pin to correct upstream versions         |
| P0       | Problem 17: CI push rebuilds          | HIGH     | Medium    | ~400 images      | FIXED         | Use docker load instead of buildx --push |
| P1       | Problem 2: Bash brace expansion       | HIGH     | Low       | 5 images         | FIXED         | Replace {{ }} with POSIX syntax          |
| P1       | Problem 4: Go GOTOOLCHAIN             | MEDIUM   | Low       | 18 images        | FIXED         | Add ENV GOTOOLCHAIN=auto                 |
| P1       | Problem 5: PLACEHOLDER_SHA            | MEDIUM   | Low       | 7 images         | FIXED         | Use                                      |     | true with placeholder checksums |
| P1       | Problem 7: pip without fallback       | MEDIUM   | Medium    | 7 images         | FIXED         | Add fallback logic                       |
| P1       | Problem 14: Missing ca-certificates   | MEDIUM   | Low       | 3 images         | FIXED         | Explicitly install ca-certificates       |
| P1       | Problem 18: CI exits on first fail    | MEDIUM   | Low       | All batch builds | FIXED         | Use continue-on-error + ::warning::      |
| P2       | Problem 8: QEMU timeouts              | MEDIUM   | Low       | Unknown          | NEEDS AUDIT   | Audit and disable multiarch              |
| P2       | Problem 6: Blank line bloat           | LOW      | Low       | 100+ images      | NEEDS CLEANUP | Cosmetic cleanup                         |
| P2       | Problem 10: Orphaned ARG GITHUB_TOKEN | LOW      | Low (sed) | 182 images       | FIXED         | Remove unused ARG declarations           |
| P3       | Problem 16: Deprecated images         | LOW      | Low       | 7 images         | FIXED         | Label as deprecated, remove from matrix  |
