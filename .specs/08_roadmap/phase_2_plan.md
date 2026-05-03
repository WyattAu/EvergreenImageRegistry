# =============================================================================
# PHASE 2: RUNTIME SECURITY HARDENING - Detailed Execution Plan
# =============================================================================
# Version: 1.0.0
# Status: PENDING
# Author: Nexus (Principal Systems Architect)
# Date: 2026-04-19
#
# ABSTRACT: This phase generates per-image runtime security profiles for Tier 1
# images (seccomp and AppArmor), enforces binary hardening (symbol stripping,
# static linking verification), implements Linux capabilities auditing
# (cap-drop ALL with documented exceptions), and adds image size enforcement
# to CI. Phase 1 must pass all quality gates before this phase begins.
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

### 1.1 Tier Classification

| Tier | Base Image | Count | Runtime Profile Priority |
|------|-----------|-------|--------------------------|
| Tier 1 | `FROM scratch` | ~104 | CRITICAL — full profiles |
| Tier 1 | `FROM gcr.io/distroless/*` | ~7 | CRITICAL — full profiles |
| Tier 2 | `FROM debian:bookworm-slim` | ~87 | HIGH — standard profiles |
| Tier 2 | `FROM cgr.dev/chainguard/wolfi-base` | ~13 | HIGH — standard profiles |
| Tier 3 | Other/Official | ~12 | MEDIUM — baseline only |

**This phase focuses on Tier 1 images (~111 images).** Tier 2 and Tier 3 profiles are deferred to Phase 5 (Military Compliance) for STIG alignment.

### 1.2 Current Runtime Security Posture

| Feature | Status | Coverage |
|---------|--------|----------|
| Seccomp profiles | MISSING | 0 images |
| AppArmor profiles | MISSING | 0 images |
| Symbol stripping | MISSING | 0 images verified |
| Static linking verification | MISSING | 0 images verified |
| Capabilities audit | MISSING | 0 images tested |
| Image size enforcement | PARTIAL | `build.yml:277-311` exists but non-blocking (warnings only) |
| USER directive | COMPLETE | All images use UID 65534 or nonroot |
| HEALTHCHECK | COMPLETE (post-Phase 0) | All images |

### 1.3 Representative Tier 1 Image Analysis

**nginx (scratch):**
```dockerfile
FROM scratch
COPY --from=downloader /nginx /nginx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
ENTRYPOINT ["/nginx"]
```
- Binary: `/nginx` (dynamically linked, needs glibc)
- Syscalls needed: read, write, open, close, epoll, socket, bind, listen, accept, etc.
- Network: TCP (port 80, 443), DNS resolution
- Filesystem: read config, write logs, write cache

**caddy (scratch):**
```dockerfile
FROM scratch
COPY --from=downloader /caddy /caddy
USER 65534:65534
ENTRYPOINT ["/caddy"]
```
- Binary: `/caddy` (statically linked by default)
- Syscalls needed: read, write, open, close, epoll, socket, bind, listen, accept, etc.
- Network: TCP (port 80, 443, 2019), TLS, DNS
- Filesystem: read config, write data, ACME certificate storage

**envoy (distroless):**
```dockerfile
FROM gcr.io/distroless/cc-debian12@sha256:af49995f9f06255ca7d955735e5484a92018f4cfe95910952d9aee165cb96940
COPY --from=downloader /envoy /envoy
USER nonroot
ENTRYPOINT ["/envoy"]
```
- Binary: `/envoy` (statically linked by default)
- Syscalls needed: extensive (gRPC, HTTP/2, TCP proxying)
- Network: TCP, UDP, Unix domain sockets
- Filesystem: read config, write access logs

### 1.4 Key Gaps

| Gap | Impact | Images Affected |
|-----|--------|-----------------|
| No seccomp profiles | Containers can invoke any syscall | 111 Tier 1 |
| No AppArmor profiles | No filesystem confinement | 111 Tier 1 |
| Unstripped binaries | Symbol table leakage, larger images | ~107 (scratch) |
| Unverified linking | Potential for dynamic library attacks | 111 Tier 1 |
| All Linux capabilities available | Unnecessary attack surface | All 223 |
| No size enforcement | Image bloat goes undetected | All 223 |

---

## 2. Task Inventory

### Dependency Graph (Topological Order)

```
Phase 1 (all gates passed)
    |
    +--> T2.1.1 (Seccomp profiles) ──> Depends on T0.3.1
    +--> T2.1.2 (AppArmor profiles) ──> Depends on T0.3.1
    +--> T2.2.1 (Symbol stripping) ──> Depends on T0.3.1
    +--> T2.2.2 (Static linking) ──> Depends on T0.3.1
    +--> T2.2.3 (Capabilities audit) ──> Depends on T0.3.1
    +--> T2.3.1 (Size enforcement) ──> Independent
```

### Parallel Execution Opportunities

```
Stream A: Seccomp Profiles (T2.1.1) — 20 hours, sequential per image type
Stream B: AppArmor Profiles (T2.1.2) — 16 hours, sequential per image type
Stream C: Binary Hardening (T2.2.1, T2.2.2) — 8 hours combined
Stream D: Capabilities (T2.2.3) — 4 hours
Stream E: Size Enforcement (T2.3.1) — 2 hours
```

All streams can execute in parallel. Streams A and B share the same dependency (T0.3.1) but do not depend on each other.

### Effort Estimate Summary

| Task | Estimated Hours | Parallel? |
|------|----------------|-----------|
| T2.1.1 | 20 | Yes (with B) |
| T2.1.2 | 16 | Yes (with A) |
| T2.2.1 | 4 | Yes |
| T2.2.2 | 4 | Yes |
| T2.2.3 | 4 | Yes |
| T2.3.1 | 2 | Yes |
| **Total** | **50** | **~24 hours wall-clock** |

---

## 3. Detailed Task Specifications

### 3.1 T2.1.1: Generate default seccomp profiles for Tier 1 images

#### Problem Analysis

Seccomp (secure computing mode) restricts the system calls a container process can invoke. Without seccomp profiles, containers run with the default Docker seccomp profile (which still allows ~300+ syscalls). For hardened images, we need per-image profiles that whitelist only the syscalls each binary actually needs.

**Challenge:** 111 Tier 1 images cannot all be profiled manually. We need an automated approach:
1. Run each image with `strace` during functional tests
2. Capture all syscalls
3. Generate a seccomp profile that whitelists only observed syscalls
4. Add a safety margin for edge cases (signal handling, etc.)

#### Solution: Automated Seccomp Profile Generation

**Profile generation pipeline:**

```
1. Start container with strace -f -e trace=%syscall
2. Run functional tests against container
3. Parse strace output to extract unique syscalls
4. Generate seccomp.json with whitelist
5. Test container with seccomp profile applied
6. If tests pass: commit profile
7. If tests fail: add missing syscalls, retry
```

**Seccomp profile format** (`images/nginx/seccomp.json`):
```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "defaultErrnoRet": 1,
  "architectures": ["SCMP_ARCH_X86_64", "SCMP_ARCH_AARCH64"],
  "syscalls": [
    {
      "names": [
        "read", "write", "open", "close", "fstat",
        "epoll_create", "epoll_ctl", "epoll_wait",
        "socket", "bind", "listen", "accept", "accept4",
        "connect", "sendto", "recvfrom", "sendmsg", "recvmsg",
        "poll", "select",
        "mmap", "munmap", "mprotect", "brk",
        "futex", "set_robust_list", "gettid",
        "clock_gettime", "nanosleep",
        "exit_group", "exit",
        "rt_sigaction", "rt_sigprocmask", "sigaltstack",
        "clone", "wait4",
        "getpid", "getuid", "getgid", "geteuid", "getegid",
        "stat", "lstat", "access",
        "writev", "readv",
        "ioctl",
        "getsockname", "getpeername", "shutdown",
        "openat", "newfstatat", "fstatat",
        "pread64", "pwrite64",
        "lseek", "fcntl",
        "getrandom",
        "uname",
        "arch_prctl"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

#### Categorized Syscall Baselines

| Image Category | Additional Syscalls | Notes |
|---------------|---------------------|-------|
| Web servers (nginx, caddy, traefik) | `inotify_init`, `inotify_add_watch`, `inotify_rm_watch` | Config file reload |
| Proxies (envoy, haproxy) | `setsockopt`, `getsockopt` | TCP tuning |
| Databases (not Tier 1) | N/A | Handled in Tier 2 |
| CLI tools (cosign, trivy, restic) | Minimal — mostly read/write/exit | May need `execve` for subprocesses |
| Monitoring (prometheus, node-exporter) | `inotify_*` | File discovery |

#### Implementation Steps

1. **Create profile generation script** (`scripts/generate_seccomp.sh`):
   ```bash
   #!/bin/bash
   IMAGE="$1"
   OUTPUT="$2"
   
   # Run container with strace, capture syscalls
   docker run --rm -d --name seccomp-capture \
     --security-opt seccomp=unconfined \
     "$IMAGE" sleep 30 2>/dev/null || \
   docker run --rm -d --name seccomp-capture \
     "$IMAGE" &
   
   PID=$(docker inspect --format '{{.State.Pid}}' seccomp-capture)
   
   # Trace all syscalls
   timeout 10 strace -f -p "$PID" -e trace=%syscall -o /tmp/strace.out 2>&1 || true
   
   # Extract unique syscalls
   SYSCALLS=$(awk '{print $2}' /tmp/strace.out | sort -u | grep -v '^\s*$' | grep -v '---')
   
   # Generate JSON profile
   python3 scripts/seccomp_generator.py \
     --syscalls "$SYSCALLS" \
     --output "$OUTPUT"
   
   docker stop seccomp-capture 2>/dev/null || true
   ```

2. **Create seccomp generator Python script** (`scripts/seccomp_generator.py`):
   - Takes list of syscalls, outputs seccomp JSON
   - Includes safe baseline syscalls (exit, rt_sigaction, etc.)
   - Supports both x86_64 and aarch64 architectures
   - Sets `defaultAction: SCMP_ACT_ERRNO`

3. **Create seccomp validation script** (`scripts/validate_seccomp.sh`):
   - Runs container with generated seccomp profile
   - Executes functional tests
   - Reports any denied syscalls
   - Automatically adds missing syscalls and regenerates

4. **Batch process all Tier 1 images**:
   ```bash
   for image in $(find images -name Dockerfile -exec grep -l 'FROM scratch\|FROM gcr.io/distroless' {} \;); do
     dir=$(dirname "$image")
     name=$(basename "$dir")
     echo "Generating seccomp profile for $name..."
     bash scripts/generate_seccomp.sh "$name" "${dir}/seccomp.json"
   done
   ```

5. **CI integration**: Test each image with its seccomp profile:
   ```yaml
   - name: Test with seccomp profile
     run: |
       SECCOMP="images/${image}/seccomp.json"
       if [ -f "$SECCOMP" ]; then
         docker run --rm --security-opt seccomp="$SECCOMP" "$REF" /nginx -v
       fi
   ```

#### Verification Criteria

- [ ] All Tier 1 images have `seccomp.json` in their image directory
- [ ] `defaultAction` is `SCMP_ACT_ERRNO` (deny by default)
- [ ] Profile includes both x86_64 and aarch64 architectures
- [ ] Container starts and passes HEALTHCHECK with profile applied
- [ ] Functional tests pass with profile applied
- [ ] No `SCMP_ACT_ALLOW` on dangerous syscalls: `execve`, `mount`, `ptrace`, `keyctl`, `userfaultfd`, `bpf`

---

### 3.2 T2.1.2: Generate AppArmor profiles for Tier 1 images

#### Problem Analysis

AppArmor provides mandatory access control (MAC) that confines:
- Filesystem access (read/write/execute paths)
- Network access (allowed protocols, ports)
- Capability usage
- Signal handling
- Ptrace/execution restrictions

Without AppArmor, a compromised container process can access any file within its mount namespace and make any network connection.

#### Solution: Per-Image AppArmor Profiles

**Profile format** (`images/nginx/apparmor_profile`):
```
#include <tunables/global>

profile evergreen-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Network access
  network inet tcp,
  network inet6 tcp,
  network inet udp,           # DNS resolution

  # Capability restrictions
  deny capability sys_admin,
  deny capability net_raw,
  deny capability sys_ptrace,
  deny capability dac_override,
  deny capability dac_read_search,

  # Filesystem access
  / r,
  /app/** r,
  /var/log/nginx/** rw,
  /var/cache/nginx/** rw,
  /etc/ssl/certs/** r,
  /etc/resolv.conf r,
  /dev/null rw,
  /dev/urandom r,
  /proc/** r,

  # Deny sensitive paths
  deny /etc/shadow r,
  deny /etc/passwd r,
  deny /proc/*/mem rw,
  deny /sys/** r,

  # Signal handling
  signal (receive) set=hup,
  signal (receive) set=term,
  signal (receive) set=usr1,

  # No exec from writable paths
  deny @{PROC}/@{pid}/cmdline r,

  # Allow execution of the main binary
  /nginx ixr,

  # Ptrace restrictions
  deny ptrace,
}
```

#### Categorized Profile Templates

| Image Category | Network | Filesystem Writes | Special |
|---------------|---------|-------------------|---------|
| Web servers | TCP 80,443 | logs/, cache/ | HUP signal for reload |
| Proxies | TCP (all) | logs/, cache/ | setsockopt for tuning |
| DNS servers | UDP 53, TCP 53 | cache/ | None |
| CLI tools | None (ephemeral) | /tmp/ | May need execve |
| Monitoring | TCP (outbound) | data/ | None |

#### Implementation Steps

1. **Create AppArmor template generator** (`scripts/generate_apparmor.sh`):
   ```bash
   #!/bin/bash
   IMAGE_NAME="$1"
   BINARY="$2"
   WRITE_PATHS="$3"   # Comma-separated
   NETWORK="$4"        # "tcp", "udp", "tcp,udp", "none"
   PORTS="$5"          # Comma-separated

   cat > "images/${IMAGE_NAME}/apparmor_profile" << AAEOF
   #include <tunables/global>
   
   profile evergreen-${IMAGE_NAME} flags=(attach_disconnected,mediate_deleted) {
     #include <abstractions/base>
     
     # Network
     $(for proto in $(echo "$NETWORK" | tr ',' ' '); do
       echo "  network inet ${proto},"
       echo "  network inet6 ${proto},"
     done)
     
     # Deny dangerous capabilities
     deny capability sys_admin,
     deny capability net_raw,
     deny capability sys_ptrace,
     deny capability dac_override,
     deny capability dac_read_search,
     deny capability setuid,
     deny capability setgid,
     
     # Read-only filesystem
     / r,
     /etc/ssl/certs/** r,
     /etc/resolv.conf r,
     /dev/null rw,
     /dev/urandom r,
     /proc/** r,
     
     # Write paths
     $(for path in $(echo "$WRITE_PATHS" | tr ',' ' '); do
       echo "  ${path}/** rw,"
     done)
     
     # Deny sensitive paths
     deny /etc/shadow r,
     deny /etc/passwd r,
     deny /proc/*/mem rw,
     deny /sys/** r,
     
     # Main binary
     /${BINARY} ixr,
     
     # No ptrace
     deny ptrace,
   }
   AAEOF
   ```

2. **Create per-image AppArmor configs** using test_runner.sh config data:
   - Extract binary name, ports, and filesystem needs from existing configs
   - Generate appropriate profiles for each Tier 1 image

3. **Test profiles** using `aa-exec`:
   ```bash
   # Load profile
   sudo apparmor_parser -r images/nginx/apparmor_profile
   
   # Test container with profile
   docker run --rm --security-opt "apparmor=evergreen-nginx" nginx -v
   ```

4. **CI integration**: Test each Tier 1 image with its AppArmor profile in CI:
   ```yaml
   - name: Install and test AppArmor profiles
     run: |
       sudo apt-get install -y apparmor-utils
       for profile in images/*/apparmor_profile; do
         image=$(basename $(dirname "$profile"))
         sudo apparmor_parser -r "$profile"
         echo "Testing AppArmor profile for $image..."
       done
   ```

5. **Create profile documentation** (`docs/apparmor-profiles.md`):
   - Explain profile structure
   - Document how to customize for specific deployments
   - Include troubleshooting guide for profile violations

#### Verification Criteria

- [ ] All Tier 1 images have `apparmor_profile` in their image directory
- [ ] Profile denies dangerous capabilities (sys_admin, net_raw, sys_ptrace, etc.)
- [ ] Profile denies sensitive filesystem paths (/etc/shadow, /proc/*/mem)
- [ ] Profile allows only necessary network protocols
- [ ] Container starts and passes HEALTHCHECK with profile applied
- [ ] Functional tests pass with profile applied
- [ ] `deny ptrace` is present in all profiles

---

### 3.3 T2.2.1: Add symbol stripping to all multi-stage builds

#### Problem Analysis

The `downloader` stage in scratch/distroless images downloads pre-built binaries. These binaries include debug symbols, which:
1. Increase image size significantly (10-50% overhead)
2. Leak internal structure to attackers (function names, file paths)
3. Provide no runtime benefit in production containers

For debian-slim images that install packages via `apt-get`, the debug symbols may be in separate packages (`-dbg`) or embedded.

#### Solution: Strip in Builder Stage

**For scratch images (curl download):**

Current Dockerfile:
```dockerfile
FROM debian:bookworm-slim AS downloader
RUN curl -fsSL "..." -o /binary.tar.gz && \
    tar -xzf /binary.tar.gz -C / && rm /binary.tar.gz && chmod +x /binary

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/binary

FROM scratch
COPY --from=downloader /binary /binary
```

Updated Dockerfile:
```dockerfile
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates binutils && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "..." -o /binary.tar.gz && \
    echo "${EXPECTED_SHA256}  /binary.tar.gz" | sha256sum -c - && \
    tar -xzf /binary.tar.gz -C / && rm /binary.tar.gz && chmod +x /binary && \
    strip --strip-all /binary && \
    echo "Stripped binary: $(ls -lh /binary)"

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/binary

FROM scratch
COPY --from=downloader /binary /binary
```

**For debian-slim images (apt install):**
```dockerfile
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-17 ca-certificates binutils && \
    strip --strip-all /usr/lib/postgresql/17/bin/postgres && \
    strip --strip-all /usr/lib/postgresql/17/bin/pg_isready && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove binutils apt apt-get dpkg 2>/dev/null || true
```

#### Implementation Steps

1. **Create Dockerfile update script** (`scripts/add_symbol_stripping.sh`):
   - For each scratch/distroless Dockerfile: add `strip --strip-all` after download
   - For each debian-slim Dockerfile: add `strip` after install, before cleanup
   - Add `binutils` to package list (needed for `strip`), then remove it

2. **Handle archives (tar.gz)**: Strip after extraction, not the archive itself.

3. **Handle multi-binary archives**: Some tarballs contain multiple binaries — strip all executables:
   ```bash
   find /extracted -type f -executable -exec strip --strip-all {} \;
   ```

4. **Verify stripping** in CI:
   ```bash
   # Check that binary has no symbol table
   docker run --rm "$IMAGE" sh -c 'readelf -S /binary 2>/dev/null | grep -q ".symtab" && exit 1 || exit 0'
   # For scratch images (no shell), extract and check:
   docker create --name tmp "$IMAGE"
   docker cp tmp:/binary /tmp/binary
   docker rm tmp
   nm /tmp/binary 2>&1 | grep -q "no symbols" && echo "PASS" || echo "FAIL"
   ```

#### Verification Criteria

- [ ] All scratch/distroless images strip binaries in downloader stage
- [ ] All debian-slim images strip binaries in builder stage
- [ ] `binutils` is not present in final image
- [ ] `nm` shows "no symbols" for all binaries
- [ ] `readelf -S` shows no `.symtab` section
- [ ] Binary still functions correctly after stripping (functional tests pass)

---

### 3.4 T2.2.2: Verify and document static linking for all binaries

#### Problem Analysis

Statically linked binaries eliminate a class of attacks:
- No shared library injection (LD_PRELOAD)
- No RPATH/RUNPATH exploitation
- No dynamic linker attacks
- Smaller dependency tree

Not all binaries can be statically linked:
- Go binaries: static by default (CGO_ENABLED=0)
- Rust binaries: static by default (musl target)
- C/C++ binaries: often dynamic, may have static variants
- Java/Python/Node: always dynamic (need runtime)

#### Solution: LDD Check + Exception Documentation

**CI verification script** (`scripts/check_static_linking.sh`):
```bash
#!/bin/bash
IMAGE="$1"
BINARY="${2:-$(docker inspect --format='{{(index .Config.Entrypoint 0)}}' "$IMAGE")}"

# Extract binary from container
docker create --name static-check "$IMAGE" 2>/dev/null || true
docker cp "static-check:${BINARY}" /tmp/binary 2>/dev/null || {
  docker rm static-check 2>/dev/null
  echo "SKIP: Cannot extract binary"
  exit 0
}
docker rm static-check 2>/dev/null

# Check if dynamically linked
if file /tmp/binary | grep -q "dynamically linked"; then
  DYNAMIC_LIBS=$(ldd /tmp/binary 2>/dev/null || echo "none")
  echo "WARN: ${BINARY} is dynamically linked"
  echo "Libraries: ${DYNAMIC_LIBS}"
  exit 1
else
  echo "PASS: ${BINARY} is statically linked"
  exit 0
fi
```

**Static linking report** (`docs/static-linking-report.md`):
```markdown
# Static Linking Report

## Tier 1: Scratch Images

| Image | Binary | Static? | Notes |
|-------|--------|---------|-------|
| nginx | /nginx | NO | Needs glibc, libpcre, libz |
| caddy | /caddy | YES | Go binary, CGO_ENABLED=0 |
| traefik | /traefik | YES | Go binary |
| haproxy | /haproxy | NO | Needs glibc, libssl, libpcre |
| envoy | /envoy | YES | BoringSSL statically linked |
| consul | /consul | YES | Go binary |
| ... | ... | ... | ... |

## Tier 2: Debian-slim Images

| Image | Binary | Static? | Notes |
|-------|--------|---------|-------|
| postgresql | /usr/lib/postgresql/17/bin/postgres | NO | Requires libpq, glibc |
| redis | /usr/bin/redis-server | NO | Requires glibc, libssl |
| ... | ... | ... | ... |
```

#### Implementation Steps

1. **Create static linking check script**: Extract binary from container, run `file` and `ldd`.

2. **Run against all images**: Generate the static linking report.

3. **Document exceptions**: Images that must be dynamically linked need justification:
   - Binary does not provide a static build option
   - Static build would exclude necessary features
   - Static build is significantly larger than dynamic

4. **CI integration**: Add static linking check to verify stage:
   ```yaml
   - name: Check static linking
     run: |
       if docker run --rm "$REF" test -f /bin/sh 2>/dev/null; then
         # Has shell — check directly
         BINARY=$(docker inspect --format='{{(index .Config.Entrypoint 0)}}' "$REF")
         docker run --rm "$REF" ldd "$BINARY" 2>/dev/null && echo "DYNAMICALLY LINKED" || echo "STATIC"
       else
         # No shell — extract and check
         docker create --name tmp "$REF"
         docker cp tmp:"$BINARY" /tmp/binary
         docker rm tmp
         file /tmp/binary | grep -q "dynamically linked" && echo "DYNAMICALLY LINKED" || echo "STATIC"
       fi
   ```

#### Verification Criteria

- [ ] All Tier 1 images checked for static/dynamic linking
- [ ] Static linking report generated with per-image results
- [ ] Dynamically linked images have documented justification
- [ ] CI includes static linking check
- [ ] Report is committed to `docs/static-linking-report.md`

---

### 3.5 T2.2.3: Add capabilities audit (cap-drop ALL)

#### Problem Analysis

Linux capabilities are discrete privileges (e.g., `CAP_NET_BIND_SERVICE`, `CAP_CHOWN`) that can be granted to processes. Docker containers inherit a set of capabilities by default, many of which are unnecessary and increase attack surface.

The principle is **deny by default**: drop ALL capabilities, then add back only those that are required.

**Default Docker capabilities (should all be dropped):**
```
CAP_AUDIT_WRITE, CAP_CHOWN, CAP_DAC_OVERRIDE, CAP_FOWNER,
CAP_FSETID, CAP_KILL, CAP_MKNOD, CAP_NET_BIND_SERVICE,
CAP_NET_RAW, CAP_SETGID, CAP_SETUID, CAP_SETFCAP,
CAP_SETPCAP, CAP_NET_BIND_SERVICE
```

#### Solution: Capabilities Audit Script + Documentation

**Test script** (`images/tests/test_capabilities.sh`):
```bash
#!/bin/bash
set -euo pipefail

IMAGE="${1:?Usage: $0 <image>}"
PASS=0
FAIL=0

echo "=== Capabilities Audit: ${IMAGE} ==="

# Test 1: Container starts with --cap-drop ALL
echo "--- Test: Start with --cap-drop ALL ---"
if docker run --rm --cap-drop ALL "$IMAGE" &>/tmp/cap-test.log &
   CAP_PID=$!
   sleep 3
   if kill -0 "$CAP_PID" 2>/dev/null; then
     kill "$CAP_PID" 2>/dev/null
     echo "PASS: Container starts with --cap-drop ALL"
     PASS=$((PASS + 1))
   else
     wait "$CAP_PID" || true
     echo "FAIL: Container does not start with --cap-drop ALL"
     echo "Output: $(cat /tmp/cap-test.log)"
     FAIL=$((FAIL + 1))
   fi
fi

# Test 2: HEALTHCHECK passes with --cap-drop ALL
echo "--- Test: HEALTHCHECK with --cap-drop ALL ---"
if docker run --rm --cap-drop ALL -d --name cap-hc "$IMAGE" 2>/dev/null; then
  sleep 5
  HC=$(docker inspect --format='{{.State.Health.Status}}' cap-hc 2>/dev/null || echo "none")
  docker stop cap-hc 2>/dev/null || true
  docker rm cap-hc 2>/dev/null || true
  if [ "$HC" = "healthy" ]; then
    echo "PASS: HEALTHCHECK passes with --cap-drop ALL"
    PASS=$((PASS + 1))
  else
    echo "WARN: HEALTHCHECK status '${HC}' with --cap-drop ALL (may need start-period)"
  fi
else
  echo "WARN: Cannot start detached container for HEALTHCHECK test"
fi

# Test 3: No capabilities in effective set
echo "--- Test: Effective capabilities are empty ---"
docker run --rm --cap-drop ALL "$IMAGE" \
  sh -c 'cat /proc/1/status | grep CapEff' 2>/dev/null | \
  grep -q '0000000000000000' && {
    echo "PASS: No effective capabilities"
    PASS=$((PASS + 1))
  } || {
    echo "INFO: Some effective capabilities remain (may be required)"
  }

echo ""
echo "Results: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -gt 0 ] && exit 1
```

**Per-image capabilities documentation** (`docs/capabilities-audit.md`):
```markdown
# Capabilities Audit

## Required Capabilities by Image

| Image | Cap-drop ALL Works? | Required Capabilities | Justification |
|-------|---------------------|----------------------|---------------|
| nginx | YES | None | Pure application, no special capabilities |
| caddy | YES | None | Go binary, no special capabilities |
| traefik | YES | None | Go binary, no special capabilities |
| envoy | YES | None | Go binary, no special capabilities |
| haproxy | YES | None | Pure application |
| consul | YES | None | Go binary |
| bind | YES | `CAP_NET_BIND_SERVICE` | Needs to bind to port 53 |
| postgresql | MAYBE | `CAP_CHOWN` | May need for data directory ownership |
| redis | YES | None | Pure application |
```

#### Implementation Steps

1. **Create capabilities audit script**: Test all images with `--cap-drop ALL`.

2. **Run audit against all images**: Generate the capabilities matrix.

3. **Document required capabilities**: For images that need specific capabilities, document why.

4. **CI integration**: Add capabilities check to verify stage:
   ```yaml
   - name: Capabilities audit
     run: |
       bash images/tests/test_capabilities.sh "$REF"
   ```

5. **Update deployment documentation**: Recommend `--cap-drop ALL` for all images, with `--cap-add` for documented exceptions.

#### Verification Criteria

- [ ] All images tested with `--cap-drop ALL`
- [ ] Capabilities audit report generated
- [ ] Images that require capabilities have documented justification
- [ ] CI includes capabilities check
- [ ] Majority of Tier 1 images work with `--cap-drop ALL` (no exceptions needed)

---

### 3.6 T2.3.1: Add image size enforcement to CI

#### Problem Analysis

Current implementation in `build.yml:277-311` reports image sizes but only as a GitHub Step Summary table with emoji warnings. It does NOT block the build.

**Current behavior:**
```yaml
if [ "$SIZE_MB" -gt "$LIMIT" ]; then
  STATUS=":warning: OVER (${SIZE_MB}MB > ${LIMIT}MB)"
else
  STATUS=":white_check_mark: OK (${SIZE_MB}MB)"
fi
```

This is informational only — oversized images are pushed to the registry.

#### Solution: Blocking Size Enforcement

**Updated enforcement logic:**
```yaml
- name: Enforce image size limits
  run: |
    FAILURES=0
    IFS=',' read -ra IMAGE_LIST <<< "${{ matrix.images }}"
    for image in "${IMAGE_LIST[@]}"; do
       [ -z "$image" ] && continue
       SAFE="${image//\//-}"
       TAR="/tmp/images/${SAFE}.tar"
       [ ! -f "$TAR" ] && continue

       SIZE_MB=$(($(stat --format=%s "$TAR") / 1024 / 1024))
       DOCKERFILE="./images/${image}/Dockerfile"

       if grep -q 'FROM scratch' "$DOCKERFILE" 2>/dev/null; then
         LIMIT=50
         TIER="Tier 1 (scratch/distroless)"
         SEVERITY="error"
       elif grep -q 'FROM gcr.io/distroless' "$DOCKERFILE" 2>/dev/null; then
         LIMIT=50
         TIER="Tier 1 (scratch/distroless)"
         SEVERITY="error"
       else
         LIMIT=200
         TIER="Tier 2 (wolfi/debian-slim)"
         SEVERITY="warning"
       fi

       if [ "$SIZE_MB" -gt "$LIMIT" ]; then
         if [ "$SEVERITY" = "error" ]; then
           echo "::error::${image}: Size ${SIZE_MB}MB exceeds ${TIER} limit of ${LIMIT}MB"
           FAILURES=$((FAILURES + 1))
         else
           echo "::warning::${image}: Size ${SIZE_MB}MB exceeds ${TIER} limit of ${LIMIT}MB"
         fi
       fi
     done
     [ "$FAILURES" -gt 0 ] && exit 1
```

**Size thresholds:**

| Tier | Base Image | Hard Limit | Rationale |
|------|-----------|------------|-----------|
| Tier 1 | scratch | 50 MB | Should be binary + certs + static assets only |
| Tier 1 | distroless | 50 MB | Minimal runtime + binary |
| Tier 2 | wolfi | 100 MB | Small package set |
| Tier 2 | debian-slim | 200 MB | Larger package set (databases, etc.) |
| Tier 3 | Other | 500 MB | Complex applications (ERP, CRM) |

#### Implementation Steps

1. **Update `build.yml` size enforcement step**: Add blocking logic for Tier 1 and Tier 2.

2. **Add size tracking artifact**: Write size report as build artifact for trend analysis.

3. **Create size optimization guide** (`docs/image-size-optimization.md`):
   - Multi-stage builds: minimize final layer
   - Use `--no-install-recommends` in apt
   - Remove package manager cache
   - Use `.dockerignore`
   - Combine RUN instructions to reduce layers

4. **Add trend detection** (optional): Compare current sizes to previous build to detect regression.

#### Verification Criteria

- [ ] Tier 1 images exceeding 50MB cause build failure
- [ ] Tier 2 images exceeding 200MB cause build warning
- [ ] Size report is generated in build artifacts
- [ ] Size report is written to GitHub Step Summary
- [ ] Documentation for size optimization exists

---

## 4. Quality Gates

### Gate QG-2.1: All Tier 1 Images Have Seccomp Profile

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| Seccomp profile files exist | `seccomp.json` files / Tier 1 images | 100% |
| Default action is deny | Check `defaultAction` in all profiles | `SCMP_ACT_ERRNO` |
| Profile is valid JSON | `jq . seccomp.json` succeeds | 100% |
| Container starts with profile | Docker run with profile succeeds | 100% |
| Dangerous syscalls denied | No `execve`, `mount`, `ptrace` in allow list | 0 violations |

### Gate QG-2.2: All Tier 1 Images Have AppArmor Profile

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| AppArmor profile files exist | `apparmor_profile` files / Tier 1 images | 100% |
| Dangerous capabilities denied | Check for deny rules | 100% |
| Sensitive paths denied | Check for /etc/shadow, /proc/*/mem deny | 100% |
| Container starts with profile | Docker run with profile succeeds | 100% |

### Gate QG-2.3: All Binaries Are Stripped

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| No symbol table | `nm` shows "no symbols" | 100% for Tier 1 |
| Binary functional | HEALTHCHECK passes | 100% |
| binutils not in final image | `test -f /usr/bin/strip` fails | 100% |

### Gate QG-2.4: Static Linking Verified or Documented

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| All binaries checked | Images with linking status / Total | 100% |
| Exceptions documented | Dynamically linked images with justification | 100% |
| Report generated | `docs/static-linking-report.md` exists | Yes |

---

## 5. Risk Register

| Risk | Probability | Impact | Mitigation | Owner | Related Task |
|------|-------------|--------|------------|-------|-------------|
| Seccomp profile too restrictive (blocks valid syscalls) | HIGH | MEDIUM | Start with permissive profile, tighten iteratively; add safety margin syscalls | Nexus | T2.1.1 |
| AppArmor profile too restrictive (blocks filesystem access) | HIGH | MEDIUM | Start with read-only enforcement, add writes incrementally | Nexus | T2.1.2 |
| Stripping breaks binary (stripped binaries crash) | LOW | HIGH | Test each stripped binary; `strip --strip-unneeded` as fallback | Nexus | T2.2.1 |
| CI runner lacks AppArmor support | MEDIUM | HIGH | Use self-hosted runner with AppArmor; test in GHA first | Nexus | T2.1.2 |
| Size enforcement blocks legitimate images | MEDIUM | MEDIUM | Start with warning-only, tighten to blocking after optimization | Nexus | T2.3.1 |
| Strace captures incomplete syscall list | MEDIUM | MEDIUM | Run extended functional tests during capture; add baseline syscalls | Nexus | T2.1.1 |
| Some images genuinely need all Linux capabilities | LOW | LOW | Document in capabilities audit; use `--cap-add` per image | Nexus | T2.2.3 |

---

## 6. Rollback Procedures

### If T2.1.1 (seccomp profiles) causes widespread failures:
1. Collect all failed images and their denied syscalls
2. Add missing syscalls to affected profiles
3. If >30% of images fail: revert to default Docker seccomp, generate profiles in batches
4. Document syscall requirements per image category

### If T2.1.2 (AppArmor profiles) causes failures:
1. Check `dmesg` for AppArmor denial messages
2. Add missing permissions to affected profiles
3. If CI runner doesn't support AppArmor: use self-hosted runner or skip AppArmor in CI
4. Profiles can be tested locally and committed without CI enforcement

### If T2.2.1 (symbol stripping) breaks binaries:
1. Revert `strip --strip-all` to `strip --strip-unneeded` (preserves some symbols)
2. If binary still breaks: skip stripping for that specific binary, document exception
3. Check if binary is already stripped (Go binaries often are)

### If T2.3.1 (size enforcement) blocks too many images:
1. Revert to warning-only mode
2. Increase limits based on actual image sizes
3. Optimize Dockerfiles before re-enforcing limits

---

## 7. Success Metrics

| Metric | Current Value | Target Value | Measurement |
|--------|--------------|--------------|-------------|
| Tier 1 images with seccomp profiles | 0 (0%) | 111 (100%) | File count |
| Tier 1 images with AppArmor profiles | 0 (0%) | 111 (100%) | File count |
| Binaries with symbols stripped | 0 (0%) | ~107 (100%) | `nm` check |
| Binaries verified for static linking | 0 (0%) | 223 (100%) | `ldd` check |
| Images working with `--cap-drop ALL` | 0 (0%) | 200+ (90%) | Capabilities test |
| Tier 1 images exceeding 50MB | Unknown | 0 (0%) | Size enforcement |
| Static linking report | Missing | Complete | File exists |
| Capabilities audit report | Missing | Complete | File exists |
| Runtime security profile coverage | 0% | 50% (Tier 1) | Profile count |

---

**END OF PHASE 2 PLAN**
