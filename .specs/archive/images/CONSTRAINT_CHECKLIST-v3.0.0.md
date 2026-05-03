# Constraint Compliance Checklist - All Images

**Mission:** Hardened container images for critical infrastructure  
**Standard:** Sovereign Hardened Image Registry v18.0.0
**Classification:** OPERATIONAL SECURITY - ZERO-TRUST
**Last Updated:** 2026-05-03

> **NOTE:** This document is a historical reference from Phase 0. The authoritative
> constraint specification is now [REQUIREMENTS.md](../REQUIREMENTS.md) v4.0.0
> which superseded this checklist. Key differences from this original:
> - UID changed from 65534 to **65532** (Chainguard/wolfi standard)
> - debian-slim is **permanently banned** (replaced by wolfi)
> - Alpine is **permanently banned** in final stages
> - HEALTHCHECK replaced by HTTP probes on :9101 (see ADR-006)
> - Constraint IDs remapped: C001-C030 per unified spec
> - Base image preference: scratch > wolfi > RHEL UBI micro > UBI minimal > UBI standard

---

## MANDATORY: BASE IMAGE PRIORITY

**CRITICAL RULE:** NEVER USE ALPINE

| Priority | Base Image | When to Use | Verification |
|----------|------------|-------------|---------------|
| 1 (BEST) | `scratch` | Static binaries only | Binary only, no runtime |
| 2 | `wolfi` | Dynamic linking, shell needed | `cgr.dev/chainguard/wolfi-base` |
| 3 | `distroless` | Minimal glibc needed | `gcr.io/distroless/*` |
| 4 (FALLBACK) | `RHEL UBI micro` | glibc + FIPS needed | `registry.access.redhat.com/ubi9/ubi-micro` |

**NEVER:** Alpine Linux (`alpine:` base), debian-slim (`debian:bookworm-slim`)

---

## CONSTRAINT DEFINITIONS (C001-C020)

### CRITICAL CONSTRAINTS (Must Pass)

| ID | Constraint | Description | Method | Fail Action |
|----|------------|-------------|--------|-------------|
| **C001** | Non-root execution | UID 65534 (nobody) | USER directive | BLOCK BUILD |
| **C002** | Read-only root filesystem | No writes to root | --read-only flag | BLOCK BUILD |
| **C003** | No shell | /bin/sh, /bin/bash removed | File check | BLOCK BUILD |
| **C004** | No package manager | apt, apk, dnf removed | File check | BLOCK BUILD |
| **C007** | Zero CVEs | 0 Critical/High | Trivy scan | BLOCK BUILD |
| **C008** | Image signed | Cosign verification | Cosign | BLOCK PUSH |
| **C012** | No embedded secrets | No hardcoded secrets | Secret scan | BLOCK BUILD |

### HIGH CONSTRAINTS (Required)

| ID | Constraint | Description | Method | Fail Action |
|----|------------|-------------|--------|-------------|
| **C005** | Static linking | Statically linked binary | ldd output | WARN |
| **C006** | Stripped symbols | No DWARF sections | nm output | WARN |
| **C009** | SBOM generated | Syft output | File check | BLOCK PUSH |
| **C010** | Health check | Working /health | HTTP check | WARN |
| **C013** | OCI compliant | Image spec v1.0+ | Manifest | WARN |
| **C014** | Minimal packages | <50 packages | Package count | WARN |
| **C015** | No debug tools | gdb, strace removed | Binary check | BLOCK BUILD |

### MEDIUM CONSTRAINTS (Recommended)

| ID | Constraint | Description | Method | Fail Action |
|----|------------|-------------|--------|-------------|
| **C011** | Signal handling | SIGTERM graceful | Kill test | WARN |
| **C016** | No init system | App runs as PID 1 | Process check | INFO |
| **C017** | No Docker socket | No /var/run/docker.sock | File check | BLOCK BUILD |
| **C018** | No sudo/su | No privilege escalation | File check | BLOCK BUILD |
| **C019** | Immutable tags | Tags never overwritten | Policy | INFO |
| **C020** | User namespace isolation | Optional isolation | Check user | INFO |

---

## VERIFICATION COMMANDS

```bash
# C001: Non-root execution
docker run --rm <image> id
# Expected: uid=65534(nobody) or similar non-root

# C002: Read-only root filesystem  
docker run --rm --read-only <image> touch /test
# Expected: touch: /test: Read-only file system

# C003: No shell
docker run --rm <image> test -f /bin/sh
# Expected: exit code 1 (not found)

# C004: No package manager
docker run --rm <image> which apt apk dnf yum
# Expected: (empty - not found)

# C005: Static linking
docker run --rm <image> ldd /binary 2>&1 | grep -i "not a dynamic"
# Expected: static output or "not a dynamic"

# C006: Stripped symbols
docker run --rm <image> file /binary
# Expected: stripped

# C007: Zero CVEs
trivy image --severity CRITICAL,HIGH <image>
# Expected: 0 vulnerabilities

# C008: Image signed
cosign verify <image>
# Expected: Verification success

# C009: SBOM generated
syft <image> -o json | jq .artifacts
# Expected: JSON output

# C010: Health check
docker run -d --name test <image>
curl http://localhost:<port>/health
# Expected: 200 OK

# C011: Signal handling
docker run -d --name test <image>; sleep 2
docker kill --signal SIGTERM test
sleep 5
docker inspect test --format '{{.State.Running}}'
# Expected: false (graceful exit)

# C012: No embedded secrets  
trufflehog filesystem <image>
# Expected: 0 secrets found

# C013: OCI compliant
crane manifest <image> | jq .schemaVersion
# Expected: 2

# C014: Package count
docker run --rm <image> dpkg -l | wc -l
# Expected: <50 for non-scratch

# C015: No debug tools
docker run --rm <image> which gdb strace ltrace
# Expected: (empty - not found)

# C017: No Docker socket
docker run --rm <image> test -S /var/run/docker.sock
# Expected: exit code 1 (not found)

# C018: No sudo/su
docker run --rm <image> which sudo su
# Expected: (empty - not found)
```

---

## PRE-BUILD CHECKLIST

Before ANY Dockerfile is committed:

- [ ] Base image follows priority: scratch > distroless > wolfi > debian-slim
- [ ] Alpine NEVER used (CHECK: `grep -i "alpine" Dockerfile`)
- [ ] Download URL verified current (CHECK: curl -I URL returns 200)
- [ ] Version matches specification in generator
- [ ] USER directive sets UID 65534 (nobody)
- [ ] Shell removed AFTER user creation (ORDER MATTERS)
- [ ] Package manager explicitly removed
- [ ] HEALTHCHECK defined with appropriate interval
- [ ] Labels applied: vendor, version, tier, constraint claims

**Example correct user creation order:**
```dockerfile
RUN useradd -m -u 65534 -g '' appuser
RUN rm -f /bin/sh /bin/bash /usr/bin/sh /usr/bin/bash  # AFTER user creation
```

---

## POST-BUILD VERIFICATION

After successful build, CI MUST verify:

- [ ] C001: Non-root (UID != 0) - BLOCK on failure
- [ ] C002: Read-only filesystem works - BLOCK on failure  
- [ ] C003: No shell present - BLOCK on failure
- [ ] C004: No package manager - BLOCK on failure
- [ ] C007: Zero Critical/High CVEs - BLOCK on failure
- [ ] C008: Image signed - BLOCK push on failure
- [ ] C009: SBOM generated - BLOCK push on failure
- [ ] C010: Health check works - WARN on failure
- [ ] C012: No embedded secrets - BLOCK on failure
- [ ] C013: OCI compliant - WARN on failure
- [ ] C014: Minimal packages - WARN on failure
- [ ] C015: No debug tools - BLOCK on failure
- [ ] C017: No Docker socket - BLOCK on failure
- [ ] C018: No sudo/su - BLOCK on failure

---

## IMAGE COMPLIANCE MATRIX

### Legend

- ✅ = PASS - Verified working
- ⚠️ = WARN - Issue detected but not blocking
- ❌ = FAIL - Blocking issue
- 🔍 = PENDING - Not yet tested
- N/A = Not Applicable

### Tier 1: Gateways & Proxies

| Image | Base | C001 | C002 | C003 | C004 | C007 | C008 | C010 | Score |
|------|------|------|------|------|------|------|------|------|-------|
| traefik | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| nginx | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| haproxy | distroless | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| envoy | distroless | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| caddy | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| coredns | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

### Tier 2: Databases & Storage

| Image | Base | C001 | C002 | C003 | C004 | C007 | C008 | C010 | Score |
|------|------|------|------|------|------|------|------|------|-------|
| postgres | debian-slim | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| mysql | debian-slim | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| mariadb | debian-slim | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| redis | debian-slim | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| etcd | debian-slim | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| memcached | debian-slim | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

### Tier 3: Security & Identity

| Image | Base | C001 | C002 | C003 | C004 | C007 | C008 | C010 | Score |
|------|------|------|------|------|------|------|------|------|-------|
| vault | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| hashicorp-vault | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| keycloak | wolfi | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| openldap | wolfi | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| zitadel | wolfi | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

### Tier 4: Observability

| Image | Base | C001 | C002 | C003 | C004 | C007 | C008 | C010 | Score |
|------|------|------|------|------|------|------|------|------|-------|
| prometheus | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| loki | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| grafana | distroless | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| thanos | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| node-exporter | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| cadvisor | wolfi | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

### Tier 5: DevOps & CI/CD

| Image | Base | C001 | C002 | C003 | C004 | C007 | C008 | C010 | Score |
|------|------|------|------|------|------|------|------|------|-------|
| jenkins | debian-slim | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| argocd | wolfi | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| flux | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| tekton | wolfi | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| drone | wolfi | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

### Tier 6: Messaging

| Image | Base | C001 | C002 | C003 | C004 | C007 | C008 | C010 | Score |
|------|------|------|------|------|------|------|------|------|-------|
| rabbitmq | debian-slim | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| nats | distroless | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| activemq | wolfi | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| mqtt | wolfi | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

### Tier 7: Git & Collaboration

| Image | Base | C001 | C002 | C003 | C004 | C007 | C008 | C010 | Score |
|------|------|------|------|------|------|------|------|------|-------|
| forgejo | wolfi | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| gitea | wolfi | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| gitlab | debian-slim | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

### Tier 8: Security Tools

| Image | Base | C001 | C002 | C003 | C004 | C007 | C008 | C010 | Score |
|------|------|------|------|------|------|------|------|------|-------|
| trivy | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| syft | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| grype | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| cosign | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| step-cli | scratch | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

---

## KNOWN ISSUES & WORKAROUNDS

| Issue | Image | Root Cause | Workaround |
|-------|-------|------------|------------|
| URL 404 | traefik 3.1.4 | Version no longer at URL | Use 3.6.13 |
| Package not found | forgejo | Not in Debian repos | Use Wolfi base + binary |
| cgr.dev 403 | wolfi images | Registry auth issues | Use chainguard/wolfi-base |

---

## HARDENED IMAGE SOURCES (REFERENCE)

Before building, check these existing hardened sources:

| Source | URL | Notes |
|--------|-----|-------|
| Google Distroless | gcr.io/distroless/* | Official, trusted |
| Chainguard Images | cgr.dev/chainguard/* | Latest, actively maintained |
| Wolfi OS | cgr.dev/distroless/cc | Minimal base |
| NVIDIA NGC | ngc.nvidia.com/containers/* | GPU workloads |
| AWS ECR | public.ecr.aws/*/distroless-* | AWS official |

---

## DOCUMENT CONTROL

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-19 | Nexus | Initial constraint checklist |
| 2.0.0 | 2026-04-19 | Nexus | Added base image priority, C001-C020 |
| 3.0.0 | 2026-04-19 | Nexus | Added pre/post build checklists, matrix |

---

**END OF CONSTRAINT CHECKLIST**
**Classification: OPERATIONAL SECURITY**