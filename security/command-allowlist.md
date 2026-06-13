# Command Allowlisting Guide

## Overview

Command allowlisting restricts which commands can be executed inside a container to prevent:

- **Container escape**: Attackers running `sh`, `bash`, or other shells to explore the environment
- **Lateral movement**: Using `curl`, `wget`, `nc` to probe other services
- **Privilege escalation**: Running `su`, `sudo`, `chroot` to gain elevated access
- **Data exfiltration**: Using `scp`, `rsync`, `tar` with network capabilities
- **Persistence**: Installing backdoors via package managers or shell scripts

## Why It Matters

Evergreen images are built distroless/scratch with no shell by default. However:

1. Images using `wolfi-base` include `/bin/sh`
2. Repack images may inherit shells from upstream
3. `docker exec` bypasses ENTRYPOINT restrictions
4. Compromised processes could exec via syscalls

Defense-in-depth requires multiple layers: seccomp, AppArmor, Dockerfile hardening, and filesystem restrictions.

## Layer 1: Seccomp Profiles

Seccomp restricts available syscalls at the kernel level. Our profiles in `security/seccomp/` provide the foundation:

| Profile          | Use Case                                      | File                       |
| ---------------- | --------------------------------------------- | -------------------------- |
| `minimal.json`   | Static binaries on scratch (no networking)    | `seccomp/minimal.json`     |
| `default.json`   | General container workloads                   | `seccomp/default.json`     |
| `networking.json`| Network-facing services                       | `seccomp/networking.json`  |
| `database.json`  | Database engines                              | `seccomp/database.json`    |
| `go-runtime.json`| Go-based services                             | `seccomp/go-runtime.json`  |

### Key Restrictions

All profiles enforce:

- **No `execve`/`execveat` for arbitrary commands**: Only specific profiles allow exec
- **No `fork`/`vfork`**: Use `clone` with restricted flags only
- **No `ptrace`**: Prevents debugging and process injection (except `PTRACE_SEIZE`)
- **No `mount`/`umount`/`pivot_root`**: Prevents filesystem-based escape

### Usage

```bash
# Docker
docker run --security-opt seccomp=security/seccomp/go-runtime.json evergreen/prometheus:latest

# Kubernetes
podSpec:
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: seccomp/go-runtime.json
```

## Layer 2: AppArmor Profiles

AppArmor provides path-based mandatory access control:

| Profile                    | Use Case                              | File                                  |
| -------------------------- | ------------------------------------- | ------------------------------------- |
| `minimal.profile`          | Read-only scratch images              | `apparmor/minimal.profile`            |
| `default.profile`          | General container workloads           | `apparmor/default.profile`            |
| `docker-socket-proxy.profile` | Docker API proxying              | `apparmor/docker-socket-proxy.profile`|
| `go-runtime.profile`       | Go-based services                     | `apparmor/go-runtime.profile`         |
| `database.profile`         | Database engines                      | `apparmor/database.profile`           |

### Key Restrictions

All profiles enforce:

- **Deny `mount`, `umount`, `pivot_root`**: No filesystem manipulation
- **Deny `ptrace`**: No process debugging/injection
- **Deny `dbus`**: No IPC to system services
- **Deny raw/packet sockets**: No network-level attacks
- **Restricted file paths**: Only application-specific paths are writable

### Usage

```bash
# Docker
docker run --security-opt apparmor=evergreen-go-runtime evergreen/consul:latest

# Kubernetes
podSpec:
  securityContext:
    appArmorProfile:
      type: Localhost
      localhostProfile: evergreen-go-runtime
```

## Layer 3: ENTRYPOINT/CMD Hardening

### Fixed Command (No Shell Interpretation)

Always use the exec form to avoid shell interpretation:

```dockerfile
# CORRECT: Direct execution, no shell
ENTRYPOINT ["/binary"]
CMD ["--config", "/config/app.conf"]

# WRONG: Shell interpretation allows command injection
ENTRYPOINT /binary --config /config/app.conf
CMD /binary start
```

### No Shell in Final Stage

For `binary-download` and `source-build` images:

```dockerfile
FROM scratch
COPY --from=builder /app/binary /binary
USER 65532:65532
ENTRYPOINT ["/binary"]
```

For `repack` and `pkg-install` images using wolfi-base:

```dockerfile
FROM wolfi-base
RUN apk add --no-cache prometheus && \
    rm -rf /bin/sh /bin/bash /bin/ash /usr/bin/sh
USER 65532:65532
ENTRYPOINT ["/usr/bin/prometheus"]
CMD ["--config.file=/etc/prometheus/prometheus.yml"]
```

### Wrapper Pattern for Configuration Validation

When startup validation is needed, use a compiled wrapper instead of a shell script:

```dockerfile
# Build a minimal Go/C wrapper that validates config then execs the binary
FROM scratch
COPY --from=wrapper-builder /wrapper /entrypoint
COPY --from=upstream /app/binary /binary
USER 65532:65532
ENTRYPOINT ["/entrypoint"]
```

### Prevent Shell Access via docker exec

Use `--init` and `--read-only` flags:

```bash
docker run \
  --read-only \
  --tmpfs /tmp:noexec \
  --tmpfs /run:noexec \
  --security-opt seccomp=security/seccomp/default.json \
  --security-opt apparmor=evergreen-default \
  --init \
  evergreen/grafana:latest
```

## Layer 4: Read-Only Filesystem

A read-only root filesystem prevents:

- Writing malicious scripts
- Installing backdoor binaries
- Modifying configuration files
- Dropping exploit artifacts

### Docker

```bash
docker run \
  --read-only \
  --tmpfs /tmp:size=64m,noexec \
  --tmpfs /run:size=16m,noexec \
  --tmpfs /var/run:size=16m,noexec \
  evergreen/prometheus:latest
```

### Kubernetes

```yaml
podSpec:
  securityContext:
    readOnlyRootFilesystem: true
    runAsNonRoot: true
    runAsUser: 65532
  containers:
    - name: prometheus
      image: evergreen/prometheus:latest
      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: data
          mountPath: /data
  volumes:
    - name: tmp
      emptyDir:
        medium: Memory
        sizeLimit: 64Mi
    - name: data
      emptyDir:
        sizeLimit: 1Gi
```

## Per-Image-Category Guidance

### Databases (postgres, mysql, redis, mongodb, cockroachdb)

Databases require write access to data directories but should otherwise be locked down:

```yaml
securityContext:
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 65532
  seccompProfile:
    type: Localhost
    localhostProfile: seccomp/database.json
  appArmorProfile:
    type: Localhost
    localhostProfile: evergreen-database
```

- Use `security/seccomp/database.json` (includes `fallocate`, `sync_file_range`, `flock`)
- Use `security/apparmor/database.profile` (allows `/data/** rw`, denies `/bin/** x`)
- ENTRYPOINT must be the database binary directly, no init scripts
- Data directory mounted as a separate volume

### Proxies (nginx, envoy, traefik, haproxy)

Proxies need network access but should never execute arbitrary commands:

```yaml
securityContext:
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 65532
  seccompProfile:
    type: Localhost
    localhostProfile: seccomp/networking.json
  appArmorProfile:
    type: Localhost
    localhostProfile: evergreen-default
```

- Config mounted read-only via ConfigMap/secret
- No shell in final stage
- `--read-only` with tmpfs for `/tmp` and `/run`

### Monitoring (prometheus, grafana, alertmanager, loki)

Monitoring tools make outbound requests (SSRF risk) and must be tightly restricted:

```yaml
securityContext:
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 65532
  seccompProfile:
    type: Localhost
    localhostProfile: seccomp/go-runtime.json
  appArmorProfile:
    type: Localhost
    localhostProfile: evergreen-go-runtime
```

- Use `security/seccomp/go-runtime.json` (Go-optimized syscall set)
- Use `security/apparmor/go-runtime.profile` (allows `/data/** rw` for metrics storage)
- Apply SSRF protections from `security/ssrf-protection.md`
- Pin outbound destinations via environment variables

### Security Scanners (trivy)

Trivy needs registry access but should not reach internal services:

```yaml
securityContext:
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 65532
  seccompProfile:
    type: Localhost
    localhostProfile: seccomp/go-runtime.json
```

- Pin `TRIVY_DB_REPOSITORY` to `ghcr.io/aquasecurity/trivy-db`
- Block `169.254.169.254` and internal DNS via network policy

## Verification

### Check for Shell Access

```bash
# Verify no shell exists in the image
docker run --rm --entrypoint="" evergreen/prometheus:latest which sh && echo "FAIL" || echo "PASS"
docker run --rm --entrypoint="" evergreen/prometheus:latest which bash && echo "FAIL" || echo "PASS"

# Verify exec is blocked by seccomp
docker run --rm --security-opt seccomp=security/seccomp/go-runtime.json \
  evergreen/prometheus:latest /bin/sh -c "id" && echo "FAIL" || echo "PASS"
```

### Verify Filesystem is Read-Only

```bash
docker run --rm --read-only evergreen/grafana:latest \
  sh -c "touch /test" 2>&1 | grep -q "Read-only" && echo "PASS" || echo "FAIL"
```

### Verify with evergreenctl

```bash
evergreenctl verify --check command-allowlist images/
evergreenctl audit --security hardening images/
```
