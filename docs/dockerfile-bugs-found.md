# Dockerfile Bugs Found During SIS Deployment Debugging

This document catalogs every Dockerfile bug discovered while deploying SIS to TrueNAS. Each bug includes root cause
analysis, the fix applied, and a prevention rule to catch similar issues before they reach production.

---

## BUG-001: Missing shared libraries in scratch images

| Field               | Value          |
| ------------------- | -------------- |
| **Bug ID**          | BUG-001        |
| **Category**        | Scratch libs   |
| **Severity**        | Critical       |
| **Affected images** | `zfs-exporter` |

### Root cause

The zfs-exporter binary was dynamically linked to 20+ shared libraries including `libzfs`, `libcrypto`, `libkrb5`,
`ld-musl-x86_64.so.1`, and 16 others. The Dockerfile only copied the binary and `ca-certificates` into the scratch
stage. At runtime the dynamic linker was missing entirely, so the binary could not load any shared object and crashed
immediately on start.

### Fix applied

1. Ran `ldd /path/to/binary` on the upstream image to discover all resolved `.so` files and their paths.
2. Added `COPY --from=builder` directives for every `.so` file and the dynamic linker (`/lib/ld-*`).
3. Preserved the directory structure so the linker could find libraries at their expected absolute paths.

### Prevention rule

**Always run `ldd /path/to/binary` on the upstream image before building a scratch target.** Copy ALL resolved `.so`
files and `/lib/ld-*` into the scratch stage. Consider adding a CI check that compares `ldd` output against the list of
`COPY` directives for any scratch-based image. Alternatively, use a static build (`CGO_ENABLED=0`) or switch to a
distroless base to avoid this class of bug entirely.

---

## BUG-002: `mkdir -p /tmp/<name>` blocks binary copy

| Field               | Value                                                |
| ------------------- | ---------------------------------------------------- |
| **Bug ID**          | BUG-002                                              |
| **Category**        | Paths                                                |
| **Severity**        | Critical                                             |
| **Affected images** | `oauth2-promtail`, `promtail`, and ~40+ other images |

### Root cause

The Dockerfile contained a pattern like:

```dockerfile
RUN mkdir -p /tmp/promtail
COPY promtail /tmp/promtail
```

`mkdir -p /tmp/promtail` creates a **directory** at that path. The subsequent `COPY` then attempts to place the binary
at that same path, but since a directory already occupies it the copy either silently fails or overwrites the directory
inode. At runtime the binary is not found, causing "file not found" errors.

### Fix applied

1. Removed the `mkdir -p` for the binary destination.
2. `COPY` the binary first (which creates the file), then `mkdir -p` for any directories the binary actually needs at
   runtime (e.g., config dirs, data dirs).

```dockerfile
COPY promtail /tmp/promtail
RUN chmod +x /tmp/promtail
RUN mkdir -p /etc/promtail /var/log/promtail
```

### Prevention rule

**Never `mkdir` to the same path a binary will be `COPY`'d or `mv`'d to.** Use a different temporary directory for the
binary staging, or copy the binary before creating runtime directories. Add a CI lint rule that flags any Dockerfile
where a `mkdir` and a `COPY` share the same destination path.

---

## BUG-003: `VERSION=vX.Y.Z` combined with URL `v${VERSION}` produces `vvX.Y.Z`

| Field               | Value                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------------- |
| **Bug ID**          | BUG-003                                                                                           |
| **Category**        | Version tags                                                                                      |
| **Severity**        | High                                                                                              |
| **Affected images** | `traefik`, `alertmanager`, `cadvisor`, `crowdsec`, `element-web`, `node-exporter`, `oauth2-proxy` |

### Root cause

The Dockerfile defined `ARG VERSION=v2.10.0` (with the `v` prefix baked in), then used it in a download URL like
`https://github.com/org/repo/releases/download/v${VERSION}/binary`. Shell expansion produced `vv2.10.0`, causing a 404
during build.

### Fix applied

Stripped the `v` prefix at point of use:

```dockerfile
ARG VERSION=v2.10.0
# Option A: shell parameter expansion
RUN wget https://.../v${VERSION}/...   # REMOVED — double v
RUN wget https://.../${VERSION}/...   # CORRECT — v already in VERSION

# Option B: separate arg without prefix
ARG VERSION=v2.10.0
ARG UPSTREAM_VERSION=2.10.0
RUN wget https://.../v${UPSTREAM_VERSION}/...
```

Chose option A (remove redundant `v` from URL) as the simpler fix.

### Prevention rule

**Define `VERSION` without the `v` prefix, or be consistent about where the prefix lives.** Use `${VERSION#v}` (bash
parameter expansion) in URLs if the `v` must be preserved for tag references. Add a CI check that grep's for
`v${VERSION` or `vv` in URLs — these are almost always bugs.

---

## BUG-004: ENTRYPOINT without absolute path on scratch images

| Field               | Value     |
| ------------------- | --------- |
| **Bug ID**          | BUG-004   |
| **Category**        | Paths     |
| **Severity**        | Critical  |
| **Affected images** | `grafana` |

### Root cause

The Grafana Dockerfile used `ENTRYPOINT ["grafana-server"]` which relies on the shell's `PATH` environment variable to
locate the binary. Scratch images have no `PATH` and no shell, so the container runtime cannot resolve `grafana-server`
to an absolute path and the container fails to start.

### Fix applied

1. Ran `which grafana-server` on the upstream Grafana image to determine the installed path.
2. Changed to `ENTRYPOINT ["/usr/sbin/grafana-server"]`.

### Prevention rule

**On scratch (or distroless) images, ALWAYS use absolute paths for `ENTRYPOINT` and `CMD`.** Verify the path with
`which <binary>` on the upstream image. Add a CI check that validates all `ENTRYPOINT` and `CMD` values in scratch-stage
Dockerfiles start with `/`.

---

## BUG-005: Repackaged app images lack required init/runtime tools

| Field               | Value                          |
| ------------------- | ------------------------------ |
| **Bug ID**          | BUG-005                        |
| **Category**        | Scratch libs                   |
| **Severity**        | Critical                       |
| **Affected images** | `postgres`, `mariadb`, `redis` |

### Root cause

Evergreen repackaged PostgreSQL, MariaDB, and Redis into minimal scratch images, stripping out init tools (`initdb`,
`mysql_install_db`, `redis-cli`), shell access, shared libraries, and configuration files. These databases require a
full runtime environment with shell scripts, init tooling, and data directory initialization to function. The repackaged
images could not initialize their data directories or run startup scripts.

### Fix applied

1. Stopped repackaging database and middleware images into scratch.
2. Switched to using upstream images directly (e.g., `postgres:16`, `redis:7`).
3. Updated the image catalog to mark these as "use upstream" rather than "repackage".

### Prevention rule

**Never repackage database, middleware, or application-server images into scratch.** Only repackage simple single-binary
images (exporters, proxies, CLIs). If an image requires a shell, init scripts, or multiple runtime tools, use the
upstream image or a distroless variant as the base. Add a catalog policy that flags any image with a database, server,
or middleware category from being targeted for scratch repackaging.

---

## BUG-006: Wrong architecture binary (exec format error)

| Field               | Value                                     |
| ------------------- | ----------------------------------------- |
| **Bug ID**          | BUG-006                                   |
| **Category**        | Version tags                              |
| **Severity**        | Critical                                  |
| **Affected images** | Several Evergreen images (exact list TBD) |

### Root cause

Some Evergreen images contained binaries compiled for the wrong architecture (e.g., arm64 on an amd64 host). When Docker
tried to execute the binary on TrueNAS (amd64), the kernel returned `exec format error`. This happened because the
Dockerfile did not use `TARGETARCH` to select the correct binary variant from multi-arch releases.

### Fix applied

1. Added `ARG TARGETARCH` to Dockerfiles.
2. Used conditional logic to select the correct binary URL based on architecture:

   ```dockerfile
   ARG TARGETARCH
   RUN case "${TARGETARCH}" in \
         amd64)  ARCH="x86_64" ;; \
         arm64)  ARCH="aarch64" ;; \
       esac && \
       wget "https://.../${ARCH}/binary" -O /usr/local/bin/app
   ```

3. Added a `file <binary>` check in CI to verify the binary matches the target architecture.

### Prevention rule

**Always use `TARGETARCH` build arg for multi-arch images.** Add a `file` command check in CI that verifies the binary's
ELF architecture matches the build target. For Go binaries, set `CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH}`
explicitly.

---

## BUG-007: `cap_drop:ALL` without needed capabilities

| Field               | Value                                     |
| ------------------- | ----------------------------------------- |
| **Bug ID**          | BUG-007                                   |
| **Category**        | Permissions                               |
| **Severity**        | High                                      |
| **Affected images** | `cadvisor`, `nginx`, `oCIS collaboration` |

### Root cause

Applying `cap_drop:ALL` is a security best practice, but several containers require specific Linux capabilities to
function:

- **cadvisor**: Needs `SYS_ADMIN` to read cgroup metrics and `SYS_PTRACE` to access `/proc/<PID>/smaps`. Without these,
  the `/metrics` endpoint hangs and times out with zero data.
- **nginx**: Needs `CHOWN`, `DAC_OVERRIDE`, `SETGID`, `SETUID` to perform `chown` operations on tmpfs-mounted
  directories (e.g., `/var/cache/nginx`). Without these, nginx fails to start with "Operation not permitted".
- **oCIS collaboration**: Needs `SYS_ADMIN` for ZFS kstats access (not yet applied at time of writing).

### Fix applied

Added explicit `cap_add` for each container alongside `cap_drop:ALL`:

```yaml
services:
  cadvisor:
    cap_drop:
      - ALL
    cap_add:
      - SYS_ADMIN
      - SYS_PTRACE

  nginx:
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - DAC_OVERRIDE
      - SETGID
      - SETUID
```

### Prevention rule

**For each container, verify which Linux capabilities the application actually needs before applying `cap_drop:ALL`.**
Check application documentation, upstream Docker Compose examples, and GitHub issues for capability requirements. Start
without `cap_drop:ALL`, verify the container works, then progressively drop capabilities while testing. Maintain a
capability matrix in the image catalog.

---

## BUG-008: wolfi HAProxy 3.3.x incompatible with env var resolution

| Field               | Value                 |
| ------------------- | --------------------- |
| **Bug ID**          | BUG-008               |
| **Category**        | Version tags          |
| **Severity**        | High                  |
| **Affected images** | `docker-socket-proxy` |

### Root cause

The docker-socket-proxy service uses HAProxy from the wolfi repository as its base image. wolfi shipped HAProxy 3.3.x,
which changed how environment variables are resolved in configuration files. The docker-socket-proxy config template
references `$SOCKET_PATH` to configure the Unix socket backend, but HAProxy 3.3.x no longer performs shell-style env var
substitution on config files, causing the backend to be misconfigured and the proxy to fail.

### Fix applied

1. Pinned HAProxy to a known-working version (2.9.x series) from wolfi.
2. Added explicit env var substitution in the Dockerfile entrypoint script:

   ```bash
   export SOCKET_PATH="${SOCKET_PATH:-/var/run/docker.sock}"
   envsubst '$SOCKET_PATH' < /etc/haproxy/haproxy.cfg.template > /etc/haproxy/haproxy.cfg
   ```

3. Added a version pin in the image catalog to prevent silent upgrades.

### Prevention rule

**For config-driven services that resolve env vars, test env var substitution before shipping.** Pin to known-working
versions in the image catalog. Add integration tests that verify the service starts correctly with environment variable
overrides. Subscribe to upstream changelogs for breaking changes in major/minor version bumps.
