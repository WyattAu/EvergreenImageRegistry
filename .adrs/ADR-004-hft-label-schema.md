# Architecture Decision Record: HFT Label Schema (evergreen.hft.\*)

## ADR-004: evergreen.hft.\* Label Namespace for HFT Annotations

### Status

ACCEPTED

### Date

2026-04-20

### Author

Nexus (Principal Systems Architect)

### Context

The Evergreen Image Registry serves high-frequency trading (HFT) and ultra-low-latency environments where
microsecond-level optimization matters. Standard Docker labels are insufficient to convey HFT-specific requirements like
CPU pinning, real-time scheduling, kernel bypass capabilities, and atomic deployment strategies.

Currently, no standardized label namespace exists for HFT container annotations. This leads to:

- Ad-hoc configuration in deployment manifests
- No machine-readable HFT metadata in images
- No way for orchestration systems to auto-configure HFT parameters
- Inconsistent deployment practices across environments

This ADR establishes the `evergreen.hft.*` label namespace as the canonical way to annotate container images with
HFT-specific metadata.

### Decision

**Adopt `evergreen.hft.*` as the label prefix for all HFT-related container image annotations.**

#### Namespace Convention

All HFT labels follow the pattern:

```
evergreen.hft.<category>.<field>
```

Where `<category>` is one of: `init`, `startup`, `cpu`, `numa`, `dpdk`, `xdp`, `deploy`, `readiness`, `scheduler`,
`net`.

#### Label Schema

##### Init & Signal Handling

| Label                            | Type    | Valid Values                     | Default | Tiers | Description                          |
| -------------------------------- | ------- | -------------------------------- | ------- | ----- | ------------------------------------ |
| `evergreen.hft.init`             | enum    | `tini`, `signal-forward`, `none` | `none`  | 1, 2  | PID 1 init system for the image      |
| `evergreen.hft.init-version`     | string  | Semver (e.g. `0.19.0`)           | -       | 1     | tini version when init=tini          |
| `evergreen.hft.shutdown-timeout` | integer | `1`-`30`                         | `3`     | 1, 2  | Graceful shutdown timeout in seconds |

##### Startup Optimization

| Label                           | Type    | Valid Values          | Default | Tiers | Description                          |
| ------------------------------- | ------- | --------------------- | ------- | ----- | ------------------------------------ |
| `evergreen.hft.startup-timeout` | integer | `10`-`30000`          | -       | 1, 2  | Maximum startup time in milliseconds |
| `evergreen.hft.startup-mode`    | enum    | `hot`, `warm`, `cold` | -       | 1, 2  | Startup latency classification       |

Startup mode thresholds:

- `hot`: < 50ms (CLI tools, static binaries)
- `warm`: < 500ms (proxies, DNS resolvers, compiled daemons)
- `cold`: < 5000ms (databases, JVM applications, interpreter-based)

##### CPU & Affinity

| Label                          | Type    | Valid Values                             | Default  | Tiers | Description                  |
| ------------------------------ | ------- | ---------------------------------------- | -------- | ----- | ---------------------------- |
| `evergreen.hft.cpuset`         | string  | Docker cpuset format (`0`, `0-1`, `0,2`) | -        | 1     | Required CPU cores           |
| `evergreen.hft.cpu-shares`     | integer | `0`-`8192`                               | `1024`   | 1, 2  | CFS relative weight          |
| `evergreen.hft.cpu-quota`      | integer | microseconds                             | -        | 1     | CFS quota per period         |
| `evergreen.hft.cpu-period`     | integer | microseconds                             | `100000` | 1     | CFS scheduling period        |
| `evergreen.hft.cpu-rt-runtime` | integer | microseconds                             | -        | 1     | Real-time runtime per period |
| `evergreen.hft.cpu-rt-period`  | integer | microseconds                             | `100000` | 1     | Real-time scheduling period  |

##### NUMA Awareness

| Label                       | Type    | Valid Values                      | Default | Tiers | Description                   |
| --------------------------- | ------- | --------------------------------- | ------- | ----- | ----------------------------- |
| `evergreen.hft.numa-node`   | integer | NUMA node index                   | -       | 1     | Preferred NUMA node           |
| `evergreen.hft.numa-policy` | enum    | `bind`, `preferred`, `interleave` | -       | 1     | NUMA memory allocation policy |

##### Kernel Bypass — DPDK

| Label                          | Type | Valid Values                  | Default | Tiers                      | Description                 |
| ------------------------------ | ---- | ----------------------------- | ------- | -------------------------- | --------------------------- |
| `evergreen.hft.dpdk-capable`   | enum | `true`, `false`, `partial`    | `false` | 1                          | Whether image supports DPDK |
| `evergreen.hft.dpdk-driver`    | enum | `vfio-pci`, `uio_pci_generic` | -       | 1                          | Required DPDK driver        |
| `evergreen.hft.dpdk-hugepages` | enum | `1GB`, `2GB`                  | -       | 1                          | Required hugepage size      |
| `evergreen.hft.dpdk-numa`      | enum | `strict`, `preferred`, `none` | `none`  | NUMA requirements for DPDK |

##### Kernel Bypass — XDP

| Label                        | Type    | Valid Values          | Default | Tiers | Description                                             |
| ---------------------------- | ------- | --------------------- | ------- | ----- | ------------------------------------------------------- |
| `evergreen.hft.xdp-capable`  | boolean | `true`, `false`       | `false` | 1     | Whether image supports XDP                              |
| `evergreen.hft.xdp-mode`     | enum    | `native`, `skb`, `hw` | -       | 1     | Supported XDP hook mode                                 |
| `evergreen.hft.xdp-program`  | string  | File path             | -       | 1     | Path to bundled BPF program                             |
| `evergreen.hft.xdp-features` | string  | Comma-separated list  | -       | 1     | Required XDP features: `redirect`, `drop`, `tx`, `pass` |

##### Atomic Deployment

| Label                           | Type    | Valid Values                        | Default   | Tiers | Description                        |
| ------------------------------- | ------- | ----------------------------------- | --------- | ----- | ---------------------------------- |
| `evergreen.hft.deploy-strategy` | enum    | `blue-green`, `rolling`, `recreate` | `rolling` | 1, 2  | Deployment strategy                |
| `evergreen.hft.max-unavailable` | integer | `0`-`100`                           | `0`       | 1, 2  | Max unavailable pods during update |
| `evergreen.hft.max-surge`       | string  | integer or `N%`                     | `25%`     | 1, 2  | Max surge pods during update       |
| `evergreen.hft.ordered-startup` | integer | positive integer                    | -         | 1, 2  | Startup order in dependency chain  |

##### Readiness & Draining

| Label                            | Type    | Valid Values                             | Default | Tiers | Description                         |
| -------------------------------- | ------- | ---------------------------------------- | ------- | ----- | ----------------------------------- |
| `evergreen.hft.pre-stop-cmd`     | string  | Shell command                            | -       | 1     | Pre-stop lifecycle hook command     |
| `evergreen.hft.pre-stop-timeout` | integer | seconds                                  | `2`     | 1     | Max time for pre-stop hook          |
| `evergreen.hft.drain-timeout`    | integer | seconds                                  | `3`     | 1     | Max time for connection draining    |
| `evergreen.hft.deregister`       | enum    | `consul`, `k8s-endpoint`, `http`, `none` | `none`  | 1     | Load balancer deregistration method |
| `evergreen.hft.readiness-level`  | integer | `0`-`5`                                  | -       | 1     | Runtime readiness state             |
| `evergreen.hft.warmup-requests`  | integer | positive integer                         | -       | 1     | Requests before full readiness      |
| `evergreen.hft.warmup-duration`  | string  | Go duration (`2s`, `500ms`)              | -       | 1     | Duration before full readiness      |

Readiness levels:

- `0`: Starting (process running, not ready)
- `1`: Initializing (loading configuration)
- `2`: Warming (pre-warming connections)
- `3`: Ready (accepting traffic)
- `4`: Draining (finishing in-flight, not accepting new)
- `5`: Stopping (shutting down)

##### Real-Time Scheduling

| Label                           | Type    | Valid Values                            | Default       | Tiers | Description                         |
| ------------------------------- | ------- | --------------------------------------- | ------------- | ----- | ----------------------------------- |
| `evergreen.hft.scheduler`       | enum    | `SCHED_FIFO`, `SCHED_RR`, `SCHED_OTHER` | `SCHED_OTHER` | 1     | Linux scheduling policy             |
| `evergreen.hft.rt-priority`     | integer | `1`-`99`                                | -             | 1     | Real-time priority (1=min, 99=max)  |
| `evergreen.hft.cpu-isolation`   | boolean | `true`, `false`                         | `false`       | 1     | Requires CPU isolation (isolcpus)   |
| `evergreen.hft.irq-isolated`    | boolean | `true`, `false`                         | `false`       | 1     | Requires IRQ steering away          |
| `evergreen.hft.net-ns-mode`     | enum    | `host`, `bridge`, `none`                | `bridge`      | 1, 2  | Network namespace mode              |
| `evergreen.hft.net-ns-required` | boolean | `true`, `false`                         | `false`       | 1     | Specific network namespace required |

##### SCHED_FIFO Priority Guide

| Priority Range | Use Case                | Examples                         |
| -------------- | ----------------------- | -------------------------------- |
| 90-99          | System-critical (avoid) | Kernel threads, hardware drivers |
| 80-89          | Network I/O path        | TLS proxies, NIC-bound workers   |
| 70-79          | DNS resolution          | coredns, bind, unbound           |
| 60-69          | Encryption/tunneling    | wireguard, strongswan            |
| 50-59          | Database I/O            | postgresql, redis (SCHED_RR)     |
| 1-49           | Background RT tasks     | Monitoring agents, log shippers  |

#### Tier Applicability

| Tier                        | Labels Applied                           | Rationale                                  |
| --------------------------- | ---------------------------------------- | ------------------------------------------ |
| Tier 1 (scratch/distroless) | All labels                               | Critical path, maximum hardening           |
| Tier 2 (debian-slim/wolfi)  | Init, startup, deploy, readiness, net-ns | Important but not on critical latency path |
| Tier 3 (official/other)     | Init, deploy only                        | Baseline operational labels                |
| Tier E (external)           | None                                     | No HFT requirements                        |

#### Label Validation Rules

1. `evergreen.hft.rt-priority` is only valid when `evergreen.hft.scheduler` is `SCHED_FIFO` or `SCHED_RR`
2. `evergreen.hft.cpuset` format must match Docker cpuset syntax: single (`0`), range (`0-3`), or list (`0,2,4`)
3. `evergreen.hft.cpu-rt-runtime` must be less than `evergreen.hft.cpu-rt-period`
4. `evergreen.hft.shutdown-timeout` must be greater than `evergreen.hft.pre-stop-timeout`
5. `evergreen.hft.numa-node` must be a non-negative integer
6. `evergreen.hft.dpdk-*` labels are only valid when `evergreen.hft.dpdk-capable` is `true` or `partial`
7. `evergreen.hft.xdp-*` labels are only valid when `evergreen.hft.xdp-capable` is `true`
8. `evergreen.hft.startup-mode` must match `evergreen.hft.startup-timeout` threshold ranges

### Consequences

**Positive:**

- Standardized, machine-readable HFT metadata for all images
- Orchestration systems can auto-configure CPU pinning, scheduling, and deployment
- Clear tier-based applicability prevents label sprawl
- Validation rules prevent contradictory configurations

**Negative:**

- Label count per image increases (average 8-12 labels for Tier 1)
- Some labels require runtime infrastructure (DPDK, XDP, SCHED_FIFO)
- Label validation adds CI complexity

**Risks:**

- Labels may be ignored by non-HFT deployment environments (acceptable — labels are advisory)
- Label schema may need extension for future HFT requirements (version the schema)

### Alternatives Considered

| Alternative                          | Pros                  | Cons                                                             | Reason Rejected              |
| ------------------------------------ | --------------------- | ---------------------------------------------------------------- | ---------------------------- |
| Use `org.opencontainers.*` namespace | OCI standard          | No HFT-specific fields, requires OCI spec change                 | Too generic                  |
| Use `io.kubernetes.*` namespace      | K8s native            | K8s-specific, not portable to Docker Compose or Swarm            | Vendor lock-in               |
| Use environment variables            | Simple                | Not inspectable without running container, not in image metadata | Not machine-readable at rest |
| Use separate config files            | Unlimited flexibility | Not in image metadata, requires separate distribution            | Not self-describing          |
| Use `com.docker.*` namespace         | Docker native         | Docker-specific, not portable to other runtimes                  | Vendor lock-in               |

### Related Standards

| Standard              | Clause         | Requirement                        |
| --------------------- | -------------- | ---------------------------------- |
| OCI Image Spec        | Image Manifest | Labels in `config.Labels`          |
| OCI Distribution Spec | Manifest       | Labels are immutable per digest    |
| Docker Engine         | Labels         | `--label` flag, `org.label-schema` |
| Kubernetes            | Pod Spec       | Node affinity, resource limits     |

### Related Yellow Papers

- YP-OBSERVABILITY-001: Container Observability Theory

### Related Blue Papers

- BP-IMAGE-REGISTRY-001: Evergreen Hardened Image Registry Architecture

### Related ADRs

- ADR-001: HEALTHCHECK Strategy (readiness labels interact with HEALTHCHECK)
- ADR-003: Multi-Stage Conversion (init system affects base image choice)

### Related Constraints

- C001: Non-root user (init system must not elevate privileges)
- C002: Read-only filesystem (tini and entrypoint must not require writable paths)
- C017: No host network (net-ns-mode=host is an exception documented here)
- C018: No sudo (CAP_SYS_NICE exception for SCHED_FIFO)

### Implementation Checklist

- [ ] Define label schema (this ADR)
- [ ] Add labels to all Tier 1 Dockerfiles
- [ ] Create label validation script
- [ ] Add label validation to CI
- [ ] Create Docker Compose templates that consume labels
- [ ] Create Kubernetes templates that consume labels
- [ ] Document label usage in deployment guide
- [ ] Version the label schema (v1)

### Examples

#### Example 1: nginx (Tier 1, TLS Proxy)

```dockerfile
LABEL evergreen.hft.init="tini" \
      evergreen.hft.init-version="0.19.0" \
      evergreen.hft.shutdown-timeout="3" \
      evergreen.hft.startup-timeout="500" \
      evergreen.hft.startup-mode="warm" \
      evergreen.hft.cpuset="0-1" \
      evergreen.hft.cpu-shares="2048" \
      evergreen.hft.numa-node="0" \
      evergreen.hft.numa-policy="bind" \
      evergreen.hft.dpdk-capable="false" \
      evergreen.hft.xdp-capable="false" \
      evergreen.hft.deploy-strategy="blue-green" \
      evergreen.hft.max-unavailable="0" \
      evergreen.hft.max-surge="100%" \
      evergreen.hft.pre-stop-cmd="/nginx -s quit" \
      evergreen.hft.pre-stop-timeout="2" \
      evergreen.hft.drain-timeout="3" \
      evergreen.hft.scheduler="SCHED_FIFO" \
      evergreen.hft.rt-priority="80" \
      evergreen.hft.cpu-isolation="true" \
      evergreen.hft.irq-isolated="true"
```

#### Example 2: redis (Tier 2, Database)

```dockerfile
LABEL evergreen.hft.init="signal-forward" \
      evergreen.hft.shutdown-timeout="5" \
      evergreen.hft.startup-timeout="5000" \
      evergreen.hft.startup-mode="cold" \
      evergreen.hft.cpu-shares="2048" \
      evergreen.hft.deploy-strategy="rolling" \
      evergreen.hft.max-unavailable="0" \
      evergreen.hft.pre-stop-cmd="redis-cli SHUTDOWN NOSAVE" \
      evergreen.hft.scheduler="SCHED_RR" \
      evergreen.hft.rt-priority="50"
```

#### Example 3: trivy (Tier 3, CLI Tool)

```dockerfile
LABEL evergreen.hft.init="none" \
      evergreen.hft.startup-timeout="50" \
      evergreen.hft.startup-mode="hot" \
      evergreen.hft.deploy-strategy="recreate"
```

---

**END OF ADR-004**
