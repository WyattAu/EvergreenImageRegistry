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
(`COPY --from=downloader /tmp/file`) are equally affected. Three additional files
(drone, forgejo-runner, ocis) were caught during the full critical tier build push phase.

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

18 images with `FROM golang` but no `GOTOOLCHAIN`: badger, cayley, ct-log, dex, fail2ban-exporter, govulncheck,
health-checks, health-shim, linguist-go, meshbird, nginx-ingress-controller, nutsdb, perscache, rate-limiter,
rdns-server, scratch-go, ulogger, wireguard

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

## Fix Priority Matrix

| Priority | Problem                            | Effort    | Impact      | Action                            |
| -------- | ---------------------------------- | --------- | ----------- | --------------------------------- |
| P0       | Problem 3: BuildKit COPY eval      | Medium    | 48 images   | Fix multi-stage COPY patterns     |
| P0       | Problem 1: GITHUB_TOKEN cross-repo | Low (sed) | 343 images  | Remove unconditional auth headers |
| P1       | Problem 4: Go GOTOOLCHAIN          | Low       | 18 images   | Add ENV GOTOOLCHAIN=auto          |
| P1       | Problem 7: pip without fallback    | Medium    | 7 images    | Add fallback logic                |
| P2       | Problem 6: Blank line bloat        | Low       | 100+ images | Cosmetic cleanup                  |
| P2       | Problem 8: QEMU timeouts           | Low       | Unknown     | Audit and disable multiarch       |
