# =============================================================================
# PHASE 4: HFT HARDENING - Detailed Execution Plan
# =============================================================================
# Version: 1.0.0
# Status: PENDING
# Author: Nexus (Principal Systems Architect)
# Date: 2026-04-20
#
# ABSTRACT: This phase hardens the registry for high-frequency trading (HFT) and
# ultra-low-latency deployment scenarios. It covers startup optimization with
# signal handling and tini integration, CPU pinning and NUMA-aware affinity,
# kernel bypass patterns (DPDK/XDP), atomic deployment strategies with
# pre-stop hooks and graduated readiness, and real-time scheduling with
# SCHED_FIFO. Phase 3 must pass all quality gates before this phase begins.
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

### 1.1 Latency Budget Analysis

| Component | Target Latency | Current Measured | Gap |
|-----------|---------------|-------------------|-----|
| Signal propagation (PID 1 -> app) | < 1ms | ~5-15ms (bash default) | CRITICAL |
| Container startup to ready | < 500ms (proxies) | ~1-3s | HIGH |
| Rolling update cutover | < 100ms | ~2-5s (stop+start) | CRITICAL |
| CPU dispatch latency | < 10us | ~100us (CFS default) | HIGH |
| Network packet processing | < 5us | ~50us (kernel stack) | HIGH |
| TLS handshake | < 500us | ~2ms (software) | MEDIUM |

### 1.2 Image Categories Affected by HFT Hardening

| Category | Images | Priority | HFT Features Needed |
|----------|--------|----------|---------------------|
| TLS Proxies | nginx, envoy, traefik, haproxy, caddy | P0 | Signal, CPU pin, atomic deploy, SCHED_FIFO |
| Network Tunnels | wireguard, tailscale, netmaker, netbird | P1 | Signal, CPU pin |
| DNS | coredns, bind, unbound | P1 | Signal, CPU pin, SCHED_FIFO |
| Monitoring | prometheus, grafana, loki, victoriametrics | P2 | Signal, atomic deploy |
| Databases | postgresql, redis, mongodb | P2 | Signal, CPU pin |
| CI/CD | jenkins, argocd, tekton, drone | P3 | Signal, atomic deploy |
| VPN | strongswan, openvpn, netclient | P1 | Signal, CPU pin |
| Identity | keycloak, zitadel, headscale | P3 | Signal |
| Storage | minio, restic | P2 | Signal, atomic deploy |

### 1.3 Current Signal Handling Posture

| Aspect | Current State | Target State |
|--------|--------------|--------------|
| PID 1 signal forwarding | Missing (no tini, no entrypoint) | tini or evergreen-entrypoint.sh |
| SIGTERM -> app | N/A (app is PID 1) | < 1ms propagation |
| Graceful shutdown timeout | Docker default (10s) | Configurable 1-5s |
| SIGKILL fallback | After 10s | After configurable timeout |
| Pre-stop hooks | Missing | Configurable per-image |
| Startup timeout | Missing | Label-annotated |

---

## 2. Task Inventory

### Dependency Graph (Topological Order)

```
Phase 3 (all gates passed)
    |
    +--> T4.1.1 (evergreen-entrypoint.sh) ──> Independent
    +--> T4.1.2 (tini integration) ──> Depends on T4.1.1
    +--> T4.1.3 (startup-timeout labels) ──> Depends on T4.1.1
    |
    +--> T4.2.1 (CPU pinning labels) ──> Independent
    +--> T4.2.2 (compose manifests) ──> Depends on T4.2.1
    +--> T4.2.3 (NUMA awareness) ──> Depends on T4.2.1
    |
    +--> T4.3.1 (DPDK labels) ──> Independent
    +--> T4.3.2 (XDP labels) ──> Independent
    |
    +--> T4.4.1 (rolling update strategies) ──> Depends on T4.1.1
    +--> T4.4.2 (pre-stop hooks) ──> Depends on T4.1.1
    +--> T4.4.3 (readiness levels) ──> Depends on T4.4.1
    |
    +--> T4.5.1 (SCHED_FIFO labels) ──> Depends on T4.2.1
    +--> T4.5.2 (CAP_SYS_NICE docs) ──> Depends on T4.5.1
    +--> T4.5.3 (network namespace) ──> Depends on T4.5.1
```

### Parallel Execution Opportunities

```
Stream A: Startup Optimization (T4.1.1 -> T4.1.2 -> T4.1.3) — 12 hours
Stream B: CPU Pinning (T4.2.1 -> T4.2.2 -> T4.2.3) — 16 hours
Stream C: Kernel Bypass (T4.3.1, T4.3.2) — 8 hours
Stream D: Atomic Deploy (T4.4.1 -> T4.4.2 -> T4.4.3) — 12 hours
Stream E: Real-Time Scheduling (T4.5.1 -> T4.5.2 -> T4.5.3) — 10 hours
```

### Effort Estimate Summary

| Task | Estimated Hours | Parallel? |
|------|----------------|-----------|
| T4.1.1 | 4 | Yes |
| T4.1.2 | 4 | Yes |
| T4.1.3 | 4 | Yes |
| T4.2.1 | 6 | Yes |
| T4.2.2 | 6 | Yes |
| T4.2.3 | 4 | Yes |
| T4.3.1 | 4 | Yes |
| T4.3.2 | 4 | Yes |
| T4.4.1 | 4 | Yes |
| T4.4.2 | 4 | Yes |
| T4.4.3 | 4 | Yes |
| T4.5.1 | 4 | Yes |
| T4.5.2 | 3 | Yes |
| T4.5.3 | 3 | Yes |
| **Total** | **58** | **~16 hours wall-clock** |

---

## 3. Detailed Task Specifications

### 3.1 T4.1.1: Implement evergreen-entrypoint.sh Signal Forwarding

#### Problem Analysis

Containers where the application runs as PID 1 have two critical problems:

1. **Signal handling**: The Linux kernel delivers signals to PID 1 with special semantics. Signals that would normally terminate a process are ignored unless PID 1 has an explicit signal handler. Most compiled binaries do not install handlers for SIGTERM when running as PID 1.

2. **Zombie reaping**: PID 1 must reap orphaned child processes. Without a proper init system, zombies accumulate and eventually exhaust the process table (PID limit).

Currently, all 223 images run their application binary directly as PID 1 via `ENTRYPOINT ["/binary"]`. This means:
- SIGTERM from `docker stop` is often ignored
- Docker waits 10 seconds before SIGKILL
- The 10-second grace period is wasted time in HFT contexts
- In-flight requests are not drained during shutdown

#### Solution: Graceful Signal Forwarding Entrypoint

**File:** `scripts/evergreen-entrypoint.sh`

Design requirements:
- POSIX-compliant (sh, not bash) for maximum compatibility
- Forward SIGTERM, SIGINT, SIGQUIT to the child process
- Implement configurable shutdown timeout via `EVERGREEN_SHUTDOWN_TIMEOUT` env var (default: 3s)
- Kill with SIGKILL after timeout expires
- Reap zombie processes
- Exit with the child process's exit code

```
Container lifecycle with evergreen-entrypoint.sh:
1. evergreen-entrypoint.sh starts as PID 1
2. Spawns application binary as child process
3. Registers signal traps (SIGTERM, SIGINT, SIGQUIT)
4. On signal: forwards to child, starts timeout
5. Child exits gracefully -> entrypoint exits with child code
6. Timeout expires -> SIGKILL child, exit 143
7. No signal -> wait for child, exit with child code
```

#### Label Integration

Images using `evergreen-entrypoint.sh` receive:
```
evergreen.hft.init=signal-forward
evergreen.hft.shutdown-timeout=<seconds>
```

#### Implementation Steps

1. Write `scripts/evergreen-entrypoint.sh` (POSIX sh)
2. Test signal forwarding with 50ms, 100ms, 500ms, 1s, 3s timeouts
3. Verify zombie reaping
4. Verify exit code propagation
5. Add to non-scratch images via multi-stage COPY
6. Update Dockerfiles for Tier 1 proxy/tunnel/DNS images
7. Add CI test: verify signal propagation latency < 1ms

#### Verification Criteria

- [ ] SIGTERM forwarded to child within 1ms
- [ ] SIGINT forwarded to child within 1ms
- [ ] SIGQUIT forwarded to child within 1ms
- [ ] SIGKILL sent after configurable timeout
- [ ] Exit code matches child process exit code
- [ ] Zombie processes are reaped
- [ ] POSIX sh compatible (no bashisms)
- [ ] Script size < 100 lines

---

### 3.2 T4.1.2: Integrate tini as PID 1 for Scratch Images

#### Problem Analysis

Scratch images cannot use shell scripts as PID 1 (no `/bin/sh`). The industry-standard solution is `tini`, a minimal init system specifically designed for containers:

- ~10KB static binary
- Zero dependencies
- Signal forwarding built-in
- Zombie reaping built-in
- Option to run as process subreaper

`tini` is already embedded in Docker Desktop and is the default init in Kubernetes.

#### Solution: Embed tini in Scratch Images

**Strategy per base image type:**

| Base Image | PID 1 Strategy | Rationale |
|-----------|----------------|-----------|
| `FROM scratch` | Embed tini static binary | No shell available |
| `FROM gcr.io/distroless/*` | Embed tini static binary | No shell available |
| `FROM cgr.dev/chainguard/wolfi-base` | Use evergreen-entrypoint.sh | Shell available |
| `FROM debian:bookworm-slim` | Use evergreen-entrypoint.sh | Shell available |

**Dockerfile pattern for scratch images:**

```dockerfile
FROM debian:bookworm-slim AS tini-builder
ARG TINI_VERSION=v0.19.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-static-amd64" \
    -o /tini && chmod +x /tini

FROM scratch
COPY --from=tini-builder /tini /tini
COPY --from=builder /nginx /nginx
ENTRYPOINT ["/tini", "--", "/nginx"]
```

**tini flags:**

| Flag | Purpose | Default |
|------|---------|---------|
| `-s` | Register as process subreaper | Off |
| `-v` | Verbose logging | Off |
| `-g` | Send signal to process group | Off |
| `--` | Signal end of tini options | Required |

For HFT images, use `-g` to send signals to the entire process group (ensures all workers receive SIGTERM).

#### Label Integration

```
evergreen.hft.init=tini
evergreen.hft.init-version=0.19.0
evergreen.hft.tini-flags=-g
```

#### Implementation Steps

1. Add tini to all Tier 1 scratch/distroless images
2. Pin tini version (0.19.0)
3. Verify tini checksum in builder stage
4. Update ENTRYPOINT to `["/tini", "--", "/binary"]`
5. Add tini to CI build cache
6. Verify signal forwarding latency

#### Verification Criteria

- [ ] tini embedded in all scratch/distroless Tier 1 images
- [ ] tini version pinned and checksummed
- [ ] Signal forwarding works correctly
- [ ] Zombie processes are reaped
- [ ] Image size increase < 15KB per image
- [ ] No new vulnerabilities introduced by tini

---

### 3.3 T4.1.3: Add Startup Timeout Labels

#### Problem Analysis

In HFT environments, containers that fail to start within a defined window must be detected and replaced immediately. Current behavior:
- Docker waits indefinitely for HEALTHCHECK to pass
- No startup timeout configuration
- Orchestration systems may not detect slow-starting containers

#### Solution: Startup Timeout Labels

Define labels that annotate maximum acceptable startup time per image:

| Label | Description | Example |
|-------|-------------|---------|
| `evergreen.hft.startup-timeout` | Maximum startup time in milliseconds | `500` |
| `evergreen.hft.startup-mode` | Startup behavior classification | `cold`, `warm`, `hot` |

**Startup mode definitions:**

| Mode | Description | Timeout | Examples |
|------|-------------|---------|---------|
| `hot` | Pre-warmed, instant readiness | < 50ms | CLI tools, static binaries |
| `warm` | Fast start, brief initialization | < 500ms | Proxies, DNS resolvers |
| `cold` | Slower start, full initialization | < 5000ms | Databases, JVM apps |

**Per-category defaults:**

| Category | Default Timeout | Default Mode |
|----------|----------------|-------------|
| TLS Proxies | 500ms | warm |
| DNS | 300ms | warm |
| VPN/Tunnels | 1000ms | warm |
| Databases | 5000ms | cold |
| Monitoring | 2000ms | warm |
| CI/CD | 3000ms | cold |
| CLI Tools | 50ms | hot |

#### Implementation Steps

1. Define label schema in ADR-004
2. Add labels to all Tier 1 Dockerfiles
3. Create orchestration template that reads labels
4. Add CI validation: startup time must be within labeled timeout
5. Add startup time benchmarking (extending T3.2.2 from Phase 3)

#### Verification Criteria

- [ ] All Tier 1 images have `evergreen.hft.startup-timeout` label
- [ ] All Tier 1 images have `evergreen.hft.startup-mode` label
- [ ] Startup time measured in CI matches label
- [ ] Images exceeding timeout are flagged
- [ ] Label values documented in ADR-004

---

### 3.4 T4.2.1: Define CPU Pinning Labels

#### Problem Analysis

In HFT environments, CPU cache affinity directly impacts latency. The Linux Completely Fair Scheduler (CFS) may migrate processes between cores, causing cache misses and jitter. CPU pinning eliminates this by binding a process to specific cores.

Current state:
- No CPU pinning configuration
- No CPU affinity labels
- Docker defaults to CFS with no affinity restrictions

#### Solution: CPU Affinity Label Schema

| Label | Description | Example |
|-------|-------------|---------|
| `evergreen.hft.cpuset` | Required CPU cores (Docker cpuset format) | `0-1` |
| `evergreen.hft.cpu-shares` | Relative CPU weight (CFS shares) | `1024` |
| `evergreen.hft.cpu-quota` | CFS quota in microseconds | `100000` |
| `evergreen.hft.cpu-period` | CFS period in microseconds | `100000` |
| `evergreen.hft.cpu-rt-runtime` | Real-time runtime in microseconds | `95000` |
| `evergreen.hft.cpu-rt-period` | Real-time period in microseconds | `100000` |

**Per-category defaults:**

| Category | cpuset | cpu-shares | Rationale |
|----------|--------|------------|-----------|
| TLS Proxies | Dedicated 2 cores | 2048 | Latency-sensitive, needs dedicated cores |
| DNS | Shared 2 cores | 1024 | Moderate latency sensitivity |
| VPN/Tunnels | Dedicated 1 core | 1024 | Encryption-bound |
| Databases | Dedicated 2-4 cores | 2048 | I/O + compute |
| Monitoring | Shared cores | 512 | Not latency-critical |

**NUMA awareness labels:**

| Label | Description | Example |
|-------|-------------|---------|
| `evergreen.hft.numa-node` | Preferred NUMA node | `0` |
| `evergreen.hft.numa-policy` | NUMA allocation policy | `bind`, `preferred`, `interleave` |

#### Implementation Steps

1. Define CPU pinning label schema in ADR-004
2. Add labels to all Tier 1 Dockerfiles
3. Create docker-compose templates that read labels
4. Validate cpuset format in CI
5. Document NUMA topology requirements

#### Verification Criteria

- [ ] All Tier 1 proxy images have `evergreen.hft.cpuset` label
- [ ] CPU share values are reasonable (512-4096 range)
- [ ] cpuset format is valid Docker syntax
- [ ] NUMA labels present for database and proxy images
- [ ] Labels documented in ADR-004

---

### 3.5 T4.2.2: Create CPU-Pinned Docker Compose Manifests

#### Problem Analysis

CPU pinning configuration is runtime-specific and depends on the deployment environment. Docker Compose is the most common single-host orchestration tool for HFT environments.

#### Solution: Reference Compose Manifests

**File:** `deploy/hft/docker-compose.network.yml`

This compose file demonstrates CPU-pinned deployment for network proxy images:
- Each service has `cpuset` for dedicated cores
- `mem_limit` for memory isolation
- `cap_drop: ALL` for capability restriction
- `read_only: true` for filesystem immutability
- `stop_grace_period` for fast shutdown
- `security_opt: no-new-privileges:true`

See `deploy/hft/docker-compose.network.yml` for full manifest.

**Additional manifests:**

| File | Contents |
|------|----------|
| `deploy/hft/docker-compose.dns.yml` | coredns, bind, unbound |
| `deploy/hft/docker-compose.vpn.yml` | wireguard, tailscale, netmaker |
| `deploy/hft/docker-compose.monitoring.yml` | prometheus, grafana, loki |

#### Implementation Steps

1. Create `deploy/hft/docker-compose.network.yml` (nginx, envoy, traefik, haproxy, caddy)
2. Create `deploy/hft/docker-compose.dns.yml`
3. Create `deploy/hft/docker-compose.vpn.yml`
4. Create `deploy/hft/docker-compose.monitoring.yml`
5. Validate all compose files with `docker compose config`
6. Add CI validation step

#### Verification Criteria

- [ ] All compose files pass `docker compose config` validation
- [ ] Each service has `cpuset` configured
- [ ] Each service has `cap_drop: ALL`
- [ ] Each service has `read_only: true`
- [ ] Each service has `stop_grace_period` < 5s
- [ ] CPU assignments do not overlap between services

---

### 3.6 T4.2.3: NUMA-Aware Deployment

#### Problem Analysis

On multi-socket servers, memory access latency varies by NUMA node:
- Local memory access: ~80ns
- Remote memory access: ~120-150ns
- Cross-socket cache coherency: additional 50-100ns

For HFT workloads, this 40-70ns difference per memory access compounds across millions of operations per second.

#### Solution: NUMA Pinning Strategy

**Deployment rules:**

1. **Single NUMA node for latency-critical services**: Pin proxy and DNS containers to a single NUMA node to ensure all memory accesses are local.

2. **Interleave for throughput-oriented services**: Use `numactl --interleave=all` for databases and monitoring to distribute memory across nodes.

3. **Dedicate NUMA node for network I/O**: Pin containers handling network traffic to the NUMA node physically closest to the NIC.

**Runtime commands:**

```bash
# Pin container to NUMA node 0
docker run --cpuset-cpus=0-7 --cpuset-mems=0 ...

# Interleave memory across NUMA nodes
docker run --cpuset-cpus=0-15 --cpuset-mems=0-1 ...
```

**Label annotations:**

```
evergreen.hft.numa-node=0
evergreen.hft.numa-policy=bind
```

#### Verification Criteria

- [ ] NUMA labels defined in schema
- [ ] Documentation includes `numactl` examples
- [ ] Compose manifests include `cpuset-mems` for NUMA pinning
- [ ] Guidance for NIC proximity to NUMA node included

---

### 3.7 T4.3.1: Define DPDK Labels for Network Images

#### Problem Analysis

DPDK (Data Plane Development Kit) enables kernel bypass for packet processing, reducing latency from ~50us (kernel network stack) to ~2-5us (user-space processing). Not all images benefit from DPDK — only those performing packet-level operations.

**Images that benefit from DPDK:**

| Image | DPDK Use Case | Benefit |
|-------|--------------|---------|
| envoy | DPDK-based transport | 10x throughput, 5us latency |
| openvswitch | DPDK vSwitch | 10x throughput |
| suricata | DPDK capture | 10x capture rate |

**Images that do NOT benefit:**

| Image | Reason |
|-------|--------|
| nginx | Application-layer proxy, not packet-level |
| haproxy | Application-layer load balancer |
| caddy | Application-layer proxy |
| traefik | Application-layer proxy |

#### Solution: DPDK Readiness Labels

| Label | Description | Values |
|-------|-------------|--------|
| `evergreen.hft.dpdk-capable` | Image supports DPDK mode | `true`, `false`, `partial` |
| `evergreen.hft.dpdk-driver` | Required DPDK driver | `vfio-pci`, `uio_pci_generic` |
| `evergreen.hft.dpdk-hugepages` | Required hugepages | `2GB`, `1GB` |
| `evergreen.hft.dpdk-numa` | NUMA requirements for DPDK | `strict`, `preferred`, `none` |

#### Implementation Steps

1. Define DPDK label schema
2. Annotate envoy with DPDK labels
3. Document DPDK deployment prerequisites
4. Create DPDK-enabled compose override

#### Verification Criteria

- [ ] DPDK labels defined in schema
- [ ] envoy image annotated with DPDK labels
- [ ] DPDK deployment prerequisites documented
- [ ] Non-applicable images marked `dpdk-capable=false`

---

### 3.8 T4.3.2: Define XDP Labels for Network Images

#### Problem Analysis

XDP (eXpress Data Path) enables programmable packet processing at the earliest possible point in the Linux network stack — before SKB allocation. XDP is less invasive than DPDK (no hugepages, no dedicated NICs) but provides significant latency reduction for filtering and routing.

**XDP use cases in the registry:**

| Use Case | Images | XDP Benefit |
|----------|--------|-------------|
| Packet filtering | suricata, trivy (network scan) | Drop malicious packets before allocation |
| Load balancing | envoy, nginx | Steering packets to correct backend |
| DDoS mitigation | All network-facing | Drop flood traffic at driver level |

#### Solution: XDP Readiness Labels

| Label | Description | Values |
|-------|-------------|--------|
| `evergreen.hft.xdp-capable` | Image supports XDP mode | `true`, `false` |
| `evergreen.hft.xdp-mode` | Supported XDP mode | `native`, `skb`, `hw` |
| `evergreen.hft.xdp-program` | BPF program path (if bundled) | File path |
| `evergreen.hft.xdp-features` | Required XDP features | `redirect`, `drop`, `tx`, `pass` |

**XDP mode comparison:**

| Mode | Hook Point | Performance | NIC Requirement |
|------|-----------|-------------|-----------------|
| `native` | Driver level | Highest (~1us) | Supported NIC driver |
| `skb` | After SKB allocation | Medium (~5us) | Any NIC |
| `hw` | NIC hardware | Highest (sub-us) | Programmable NIC |

#### Implementation Steps

1. Define XDP label schema
2. Create `deploy/hft/xdp-filters/` directory with reference XDP programs
3. Document XDP deployment for network-facing images
4. Create compose override for XDP-enabled deployment

#### Verification Criteria

- [ ] XDP labels defined in schema
- [ ] Reference XDP filter programs provided
- [ ] XDP deployment documented
- [ ] Mode selection guidance provided

---

### 3.9 T4.4.1: Define Rolling Update Strategies

#### Problem Analysis

In HFT environments, deployment updates must not cause service interruption. The current approach (stop old, start new) causes:
- Connection drops during cutover
- Latency spikes during cold start
- In-flight request loss

#### Solution: Atomic Deployment Strategies

**Strategy matrix:**

| Strategy | Downtime | Complexity | Use Case |
|----------|----------|------------|----------|
| Recreate | Full restart | Lowest | Non-critical, batch jobs |
| Rolling | Zero (with overlap) | Medium | Stateful services |
| Blue/Green | Zero (instant cutover) | High | Stateful proxies |
| Canary | Zero (gradual) | Highest | Risky deployments |

**Per-category strategy:**

| Category | Default Strategy | Max Unavailable | Max Surge |
|----------|-----------------|-----------------|-----------|
| TLS Proxies | Blue/Green | 0 | 100% |
| DNS | Rolling | 0 | 25% |
| VPN/Tunnels | Rolling | 0 | 50% |
| Databases | Rolling (primary replica) | 0 | 1 |
| Monitoring | Rolling | 50% | 50% |
| CI/CD | Blue/Green | 0 | 100% |

**Label annotations:**

| Label | Description | Example |
|-------|-------------|---------|
| `evergreen.hft.deploy-strategy` | Deployment strategy | `blue-green`, `rolling`, `recreate` |
| `evergreen.hft.max-unavailable` | Max unavailable during update | `0` |
| `evergreen.hft.max-surge` | Max surge during update | `100%` |
| `evergreen.hft.ordered-startup` | Start order in dependency chain | `1`, `2`, `3` |

#### Implementation Steps

1. Define deployment strategy labels
2. Create Kubernetes Deployment templates with strategy annotations
3. Create Docker Swarm service templates
4. Add deployment validation to CI
5. Document per-category strategy selection

#### Verification Criteria

- [ ] All Tier 1 images have `evergreen.hft.deploy-strategy` label
- [ ] Proxy images use blue/green strategy
- [ ] Templates pass validation
- [ ] Max unavailable is 0 for all P0 images
- [ ] Ordered startup labels present for dependency chains

---

### 3.10 T4.4.2: Implement Pre-Stop Hooks

#### Problem Analysis

Before a container is stopped during a rolling update, it must:
1. Signal the load balancer to stop sending new connections (deregister)
2. Drain in-flight requests (finish processing)
3. Close listening sockets (reject new connections)
4. Flush buffers (write pending data)

Without pre-stop hooks, the load balancer may continue sending traffic to a container that is shutting down, causing connection errors and request loss.

#### Solution: Pre-Stop Lifecycle Hook Labels

| Label | Description | Example |
|-------|-------------|---------|
| `evergreen.hft.pre-stop-cmd` | Command to run before stop | `/nginx -s quit` |
| `evergreen.hft.pre-stop-timeout` | Max time for pre-stop hook | `2s` |
| `evergreen.hft.drain-timeout` | Max time for connection draining | `3s` |
| `evergreen.hft.deregister` | Load balancer deregistration method | `consul`, `k8s-endpoint`, `http` |

**Per-image pre-stop commands:**

| Image | Pre-Stop Command | Drain Method |
|-------|-----------------|-------------|
| nginx | `/nginx -s quit` | Wait for connections to close |
| envoy | `kill -TERM 1` | Envoy drains via listener config |
| traefik | `kill -TERM 1` | Traefik drains automatically |
| haproxy | `kill -USR1 1` | HAProxy graceful stop |
| caddy | `caddy stop --config /app/Caddyfile` | Caddy graceful shutdown |
| postgresql | `pg_ctl stop -m fast` | Fast shutdown (no new connections) |
| redis | `redis-cli SHUTDOWN NOSAVE` | Immediate shutdown |

**Kubernetes preStop hook example:**

```yaml
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "/nginx -s quit && sleep 2"]
```

**Docker Compose equivalent:**

```yaml
stop_grace_period: 3s
```

#### Implementation Steps

1. Define pre-stop hook labels
2. Add pre-stop commands to all Tier 1 proxy images
3. Create Kubernetes pod templates with lifecycle hooks
4. Test drain behavior with active connections
5. Verify zero dropped connections during rolling update

#### Verification Criteria

- [ ] All Tier 1 proxy images have `evergreen.hft.pre-stop-cmd` label
- [ ] Pre-stop hook executes before SIGTERM
- [ ] In-flight requests complete during drain period
- [ ] No connection errors during rolling update
- [ ] Load balancer deregistration completes before stop

---

### 3.11 T4.4.3: Define Readiness Levels

#### Problem Analysis

A container transitions through multiple states during startup. A simple "ready/not ready" binary is insufficient for HFT environments where partial readiness must be communicated to the orchestrator.

#### Solution: Graduated Readiness Levels

| Level | Name | Description | HEALTHCHECK Behavior |
|-------|------|-------------|---------------------|
| 0 | Starting | Process is running | Not yet checking |
| 1 | Initializing | Loading configuration | Return unhealthy |
| 2 | Warming | Pre-warming connections | Return unhealthy |
| 3 | Ready | Accepting new connections | Return healthy |
| 4 | Draining | Shutting down, finishing in-flight | Return healthy (for LB removal) |
| 5 | Stopping | No longer accepting traffic | Return unhealthy |

**Label annotations:**

| Label | Description | Example |
|-------|-------------|---------|
| `evergreen.hft.readiness-level` | Current readiness level (runtime) | `0-5` |
| `evergreen.hft.warmup-requests` | Requests to process before full readiness | `100` |
| `evergreen.hft.warmup-duration` | Duration before full readiness | `2s` |

**Implementation:**

Readiness levels are communicated via:
1. **HEALTHCHECK**: Levels 3-4 return healthy; others return unhealthy
2. **File-based**: Write level to `/tmp/evergreen-readiness` (for non-scratch images)
3. **HTTP endpoint**: Expose `/readyz?level` (for images with HTTP server)
4. **Exit code**: HEALTHCHECK returns exit code `0` (ready), `1` (not ready), `2` (warming)

#### Verification Criteria

- [ ] Readiness levels defined and documented
- [ ] HEALTHCHECK reflects readiness level
- [ ] Warmup request/duration labels defined
- [ ] Orchestrator templates consume readiness levels

---

### 3.12 T4.5.1: Define SCHED_FIFO Labels

#### Problem Analysis

The Linux CFS (Completely Fair Scheduler) introduces scheduling jitter of ~100us between process wake-ups and actual execution. For HFT workloads, this jitter is unacceptable.

SCHED_FIFO (First-In, First-Out) real-time scheduling policy:
- Eliminates scheduling jitter
- Provides deterministic execution order
- Process runs until it blocks or yields
- Priority range: 1-99 (higher = more priority)

**Risks:**
- A SCHED_FIFO process that never blocks can starve the entire system
- Requires careful priority assignment
- Requires CAP_SYS_NICE capability

#### Solution: Real-Time Scheduling Labels

| Label | Description | Example |
|-------|-------------|---------|
| `evergreen.hft.scheduler` | Linux scheduling policy | `SCHED_FIFO`, `SCHED_RR`, `SCHED_OTHER` |
| `evergreen.hft.rt-priority` | Real-time priority (1-99) | `50` |
| `evergreen.hft.cpu-isolation` | Whether CPU should be isolated | `true`, `false` |

**Priority assignment:**

| Category | Scheduler | Priority | Rationale |
|----------|-----------|----------|-----------|
| TLS Proxies (core) | SCHED_FIFO | 80 | Highest latency sensitivity |
| DNS | SCHED_FIFO | 70 | DNS resolution on critical path |
| VPN/Tunnels | SCHED_FIFO | 60 | Encryption-bound, not highest priority |
| Monitoring | SCHED_OTHER | N/A | Not latency-critical |
| Databases | SCHED_RR | 50 | Round-robin for fairness among queries |
| CI/CD | SCHED_OTHER | N/A | Not latency-critical |

**CPU isolation via kernel boot parameters:**

```
# isolcpus isolates CPU cores from the general scheduler
# nohz_full disables timer ticks on isolated cores
# rcu_nocbs moves RCU callbacks off isolated cores
isolcpus=2-3 nohz_full=2-3 rcu_nocbs=2-3
```

#### Implementation Steps

1. Define scheduling labels
2. Add labels to Tier 1 proxy and DNS images
3. Document kernel boot parameters for CPU isolation
4. Create compose override for SCHED_FIFO
5. Test scheduling latency with `cyclictest`

#### Verification Criteria

- [ ] Scheduling labels defined in schema
- [ ] Tier 1 proxy images have SCHED_FIFO labels
- [ ] Priority assignments are documented
- [ ] CPU isolation kernel parameters documented
- [ ] `cyclictest` shows < 10us max latency on isolated cores

---

### 3.13 T4.5.2: Document CAP_SYS_NICE Requirements

#### Problem Analysis

SCHED_FIFO and SCHED_RR require `CAP_SYS_NICE` (Linux capability 23). This conflicts with the constraint `cap_drop: ALL` (Phase 2, C018 extension).

#### Solution: Capability Exception Documentation

**Exception process:**

1. Document that SCHED_FIFO requires `CAP_SYS_NICE`
2. Add `CAP_SYS_NICE` to the capabilities exception list
3. Use seccomp profile to restrict `sched_setscheduler()` to only allow SCHED_FIFO/SCHED_RR
4. Restrict priority range via seccomp BPF filter

**Docker run with SCHED_FIFO:**

```bash
docker run \
  --cap-add=CAP_SYS_NICE \
  --cap-drop=ALL \
  --cpuset-cpus=2-3 \
  --security-opt seccomp=evergreen-rt.json \
  ...
```

**seccomp profile `evergreen-rt.json`:**

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "syscalls": [
    {
      "names": ["sched_setscheduler"],
      "args": [
        {
          "index": 1,
          "op": "SCMP_CMP_EQ",
          "value": 1
        },
        {
          "index": 2,
          "op": "SCMP_CMP_LE",
          "value": 80
        }
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

This allows `sched_setscheduler(policy=SCHED_FIFO, priority<=80)` but blocks all other scheduler operations.

#### Verification Criteria

- [ ] CAP_SYS_NICE exception documented
- [ ] seccomp profile restricts scheduling to allowed policies
- [ ] Priority range is bounded in seccomp filter
- [ ] `cap_drop: ALL` still applied (only CAP_SYS_NICE added back)

---

### 3.14 T4.5.3: Network Namespace Isolation for Real-Time Containers

#### Problem Analysis

Real-time containers on isolated CPUs must be protected from:
1. **Network interrupts**: NIC interrupts on isolated cores cause scheduling jitter
2. **SoftIRQ processing**: Network packet processing on isolated cores
3. **Timer interrupts**: Even with `nohz_full`, some timers remain

#### Solution: IRQ Affinity and Network Namespace Design

**IRQ steering:**

```bash
# Move all NIC IRQs to non-isolated cores
for irq in $(ls /proc/irq/ | grep -E '^[0-9]+$'); do
    if grep -q eth /proc/irq/$irq/smp_affinity 2>/dev/null; then
        echo 3 > /proc/irq/$irq/smp_affinity
    fi
done

# Verify IRQ distribution
cat /proc/interrupts | grep eth
```

**RPS/RFS configuration:**

```bash
# Disable RPS on isolated cores
echo 0 > /sys/class/net/eth0/queues/rx-0/rps_cpus

# Configure RFS to steer to non-isolated cores
echo 3 > /proc/sys/net/core/rps_sock_flow_entries
```

**Network namespace isolation:**

```yaml
services:
  nginx:
    network_mode: "host"  # For kernel bypass (DPDK/XDP)
    cap_add:
      - CAP_SYS_NICE
      - CAP_NET_ADMIN
    cap_drop:
      - ALL
    cpuset: "2-3"
```

**Label annotations:**

| Label | Description | Example |
|-------|-------------|---------|
| `evergreen.hft.irq-isolated` | Whether IRQs are steered away | `true` |
| `evergreen.hft.net-ns-mode` | Network namespace mode | `host`, `bridge`, `none` |
| `evergreen.hft.net-ns-required` | Whether specific net-ns is required | `true`, `false` |

#### Verification Criteria

- [ ] IRQ steering documented
- [ ] RPS/RFS configuration documented
- [ ] Network namespace labels defined
- [ ] `cyclictest` shows < 10us jitter with network load on non-isolated cores

---

## 4. Quality Gates

### Gate QG-4.1: Signal Forwarding Latency

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| SIGTERM propagation | Time from signal to child receipt | < 1ms |
| SIGKILL after timeout | Time from timeout to SIGKILL | < 100ms |
| Graceful shutdown completion | Time from SIGTERM to exit | < labeled timeout |
| Exit code propagation | Child exit code matches entrypoint exit code | 100% |

### Gate QG-4.2: CPU Pinning Validation

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| cpuset label presence | Tier 1 proxy/DNS images | 100% |
| CPU affinity verified | `taskset -pc` shows correct cores | 100% |
| No core overlap | Compose manifests don't share cores | 100% |
| NUMA label presence | Database/proxy images | 100% |

### Gate QG-4.3: Deployment Strategy Coverage

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| deploy-strategy label | Tier 1 images | 100% |
| max-unavailable=0 | P0 images | 100% |
| pre-stop hook defined | Tier 1 proxy images | 100% |
| Zero dropped connections | Rolling update test | 100% |

### Gate QG-4.4: Real-Time Scheduling

| Criterion | Measurement | Threshold |
|-----------|-------------|-----------|
| SCHED_FIFO label | Tier 1 proxy images | 100% |
| Scheduling jitter | cyclictest max latency | < 10us |
| CPU isolation | isolcpus configured | Yes |
| seccomp restriction | sched_setscheduler bounded | Yes |

---

## 5. Risk Register

| Risk | Probability | Impact | Mitigation | Owner | Related Task |
|------|-------------|--------|------------|-------|-------------|
| tini version introduces vulnerability | LOW | HIGH | Pin version, verify checksum, scan with trivy | Nexus | T4.1.2 |
| Signal forwarding adds latency | LOW | MEDIUM | Benchmark signal path, optimize hot path | Nexus | T4.1.1 |
| CPU pinning causes starvation | MEDIUM | HIGH | Document isolation requirements, test under load | Nexus | T4.2.1 |
| DPDK requires dedicated NICs | HIGH | LOW | Document as optional, default to XDP | Nexus | T4.3.1 |
| SCHED_FIFO process hangs system | MEDIUM | CRITICAL | seccomp bounds, CPU isolation, priority limits | Nexus | T4.5.1 |
| CAP_SYS_NICE conflicts with cap_drop | HIGH | MEDIUM | Document exception process, restrict via seccomp | Nexus | T4.5.2 |
| NUMA misconfiguration causes remote memory | MEDIUM | MEDIUM | Document NUMA topology requirements, validate | Nexus | T4.2.3 |
| Rolling update drops connections | LOW | HIGH | Pre-stop hooks, drain period, integration test | Nexus | T4.4.1 |
| Compose manifests diverge from labels | MEDIUM | MEDIUM | Generate compose from labels, validate in CI | Nexus | T4.2.2 |

---

## 6. Rollback Procedures

### If T4.1.1 (signal forwarding) causes startup failures:
1. Revert to direct ENTRYPOINT (no init system)
2. Identify which signal is causing the issue
3. Add signal-specific handling to entrypoint
4. Test with the specific image that failed

### If T4.2.1 (CPU pinning) causes performance degradation:
1. Check for core overlap between services
2. Verify NUMA topology matches cpuset assignment
3. Remove CPU pinning for affected service
4. Fall back to CPU shares (CFS) with higher weight

### If T4.5.1 (SCHED_FIFO) causes system instability:
1. Immediately revert to SCHED_OTHER
2. Check for priority inversion (lower priority RT task blocking higher)
3. Verify seccomp profile is active
4. Check that CPU isolation is correctly configured

### If T4.4.1 (rolling update) causes connection drops:
1. Increase drain timeout
2. Add pre-stop hook if missing
3. Check load balancer health check interval
4. Fall back to blue/green with manual cutover

---

## 7. Success Metrics

| Metric | Current Value | Target Value | Measurement |
|--------|--------------|--------------|-------------|
| Signal propagation latency | ~5-15ms | < 1ms | Benchmark |
| Graceful shutdown time | 10s (Docker default) | < 3s | Benchmark |
| Container startup to ready | ~1-3s (proxies) | < 500ms (proxies) | Benchmark |
| Rolling update cutover time | ~2-5s | < 100ms | Integration test |
| Dropped connections during update | Unknown | 0 | Integration test |
| CPU scheduling jitter | ~100us | < 10us | cyclictest |
| Images with tini/signal-forwarding | 0 | 111 (Tier 1) | CI count |
| Images with CPU pinning labels | 0 | 30+ (proxies, DNS, VPN) | CI count |
| Images with deployment strategy labels | 0 | 111 (Tier 1) | CI count |
| Images with SCHED_FIFO labels | 0 | 15+ (proxies, DNS) | CI count |

---

## Appendix A: HFT Label Schema Reference

### Complete `evergreen.hft.*` Label Namespace

| Label | Type | Default | Applicable Tiers | Description |
|-------|------|---------|-----------------|-------------|
| **Init & Signal** | | | | |
| `evergreen.hft.init` | enum | - | 1,2 | `tini`, `signal-forward`, `none` |
| `evergreen.hft.init-version` | string | - | 1 | tini version (e.g. `0.19.0`) |
| `evergreen.hft.shutdown-timeout` | int | `3` | 1,2 | Graceful shutdown timeout in seconds |
| **Startup** | | | | |
| `evergreen.hft.startup-timeout` | int | - | 1,2 | Max startup time in milliseconds |
| `evergreen.hft.startup-mode` | enum | - | 1,2 | `hot` (<50ms), `warm` (<500ms), `cold` (<5000ms) |
| **CPU & NUMA** | | | | |
| `evergreen.hft.cpuset` | string | - | 1 | Required CPU cores (Docker format) |
| `evergreen.hft.cpu-shares` | int | `1024` | 1,2 | CFS shares |
| `evergreen.hft.cpu-quota` | int | - | 1 | CFS quota in microseconds |
| `evergreen.hft.cpu-period` | int | `100000` | 1 | CFS period in microseconds |
| `evergreen.hft.cpu-rt-runtime` | int | - | 1 | Real-time runtime in microseconds |
| `evergreen.hft.cpu-rt-period` | int | `100000` | 1 | Real-time period in microseconds |
| `evergreen.hft.numa-node` | int | - | 1 | Preferred NUMA node |
| `evergreen.hft.numa-policy` | enum | - | 1 | `bind`, `preferred`, `interleave` |
| **Kernel Bypass** | | | | |
| `evergreen.hft.dpdk-capable` | enum | `false` | 1 | `true`, `false`, `partial` |
| `evergreen.hft.dpdk-driver` | string | - | 1 | `vfio-pci`, `uio_pci_generic` |
| `evergreen.hft.dpdk-hugepages` | string | - | 1 | `1GB`, `2GB` |
| `evergreen.hft.dpdk-numa` | enum | `none` | 1 | `strict`, `preferred`, `none` |
| `evergreen.hft.xdp-capable` | bool | `false` | 1 | Whether XDP is supported |
| `evergreen.hft.xdp-mode` | enum | - | 1 | `native`, `skb`, `hw` |
| `evergreen.hft.xdp-program` | string | - | 1 | BPF program path |
| `evergreen.hft.xdp-features` | string | - | 1 | Comma-separated: `redirect,drop,tx,pass` |
| **Deployment** | | | | |
| `evergreen.hft.deploy-strategy` | enum | `rolling` | 1,2 | `blue-green`, `rolling`, `recreate` |
| `evergreen.hft.max-unavailable` | int | `0` | 1,2 | Max unavailable during update |
| `evergreen.hft.max-surge` | string | `25%` | 1,2 | Max surge during update |
| `evergreen.hft.ordered-startup` | int | - | 1,2 | Start order in dependency chain |
| **Readiness & Draining** | | | | |
| `evergreen.hft.pre-stop-cmd` | string | - | 1 | Pre-stop hook command |
| `evergreen.hft.pre-stop-timeout` | int | `2` | 1 | Pre-stop hook timeout in seconds |
| `evergreen.hft.drain-timeout` | int | `3` | 1 | Connection drain timeout in seconds |
| `evergreen.hft.deregister` | enum | - | 1 | `consul`, `k8s-endpoint`, `http` |
| `evergreen.hft.readiness-level` | int | - | 1 | Runtime readiness (0-5) |
| `evergreen.hft.warmup-requests` | int | - | 1 | Warmup request count |
| `evergreen.hft.warmup-duration` | string | - | 1 | Warmup duration (e.g. `2s`) |
| **Real-Time Scheduling** | | | | |
| `evergreen.hft.scheduler` | enum | `SCHED_OTHER` | 1 | `SCHED_FIFO`, `SCHED_RR`, `SCHED_OTHER` |
| `evergreen.hft.rt-priority` | int | - | 1 | Real-time priority (1-99) |
| `evergreen.hft.cpu-isolation` | bool | `false` | 1 | Whether CPU isolation is required |
| `evergreen.hft.irq-isolated` | bool | `false` | 1 | Whether IRQs should be steered away |
| `evergreen.hft.net-ns-mode` | enum | `bridge` | 1,2 | `host`, `bridge`, `none` |
| `evergreen.hft.net-ns-required` | bool | `false` | 1 | Whether specific net-ns is required |

---

**END OF PHASE 4 PLAN**
