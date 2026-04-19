# Constraint Compliance Checklist - All Images

**Mission:** Hardened container images for critical infrastructure  
**Standard:** Sovereign Hardened Image Registry v2.0.0  
**Classification:** OPERATIONAL SECURITY

---

## Constraint Definitions

| ID | Constraint | Description | Method | Severity |
|----|------------|-------------|---------|----------|
| C001 | Non-root execution | UID 65534 (nobody) | USER directive | CRITICAL |
| C002 | Read-only root filesystem | No writes to root | --read-only flag | CRITICAL |
| C003 | No shell | /bin/sh, /bin/bash removed | File check | CRITICAL |
| C004 | No package manager | apt, apk, dnf removed | File check | CRITICAL |
| C005 | Static linking | Statically linked binary | ldd output | HIGH |
| C006 | Stripped symbols | No DWARF sections | nm output | HIGH |
| C007 | Zero CVEs | 0 Critical/High | Trivy scan | CRITICAL |
| C008 | Image signed | Cosign verification | Cosign | CRITICAL |
| C009 | SBOM generated | Syft output | File check | HIGH |
| C010 | Health check | Working /health | HTTP check | HIGH |
| C011 | Signal handling | SIGTERM graceful | Kill test | MEDIUM |
| C012 | No embedded secrets | No hardcoded secrets | Secret scan | CRITICAL |
| C013 | OCI compliant | Image spec v1.0+ | Manifest | HIGH |

---

## Verification Methods

```bash
# C001: Non-root execution
docker run --rm <image> id
# Expected: uid=65534(nobody) or similar non-root

# C002: Read-only root filesystem
docker run --rm --read-only <image> touch /test
# Expected: touch: /test: Read-only file system

# C003: No shell
docker run --rm <image> ls /bin/sh
# Expected: ls: /bin/sh: No such file or directory

# C004: No package manager
docker run --rm <image> which apt apk dnf
# Expected: (empty - not found)

# C005: Static linking
docker run --rm <image> ldd /binary 2>&1 | grep -i "not a dynamic"
# Expected: static output or "not a dynamic"

# C006: Stripped symbols
docker run --rm <image> nm /binary | wc -l
# Expected: 0 or minimal

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
docker run -d --name test <image>; sleep 2; docker kill --signal SIGTERM test; sleep 5; docker inspect test --format '{{.State.Running}}'
# Expected: false (graceful exit)

# C012: No embedded secrets  
trufflehog filesystem <image>
# Expected: 0 secrets found

# C013: OCI compliant
crane manifest <image> | jq .schemaVersion
# Expected: 2
```

---

## Image Compliance Matrix

### Legend
- ✅ = Achieved
- ⚠️ = Workaround Applied  
- ❌ = Not Achieved (requires Round 2)
- 🔍 = To Be Discovered/Verified
- N/A = Not Applicable

---

## Tier 1: Gateways & Proxies

| Image | Base | C001 | C002 | C003 | C004 | C005 | C006 | C007 | C008 | C009 | C010 | C011 | C012 | C013 | Score |
|------|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|-------|
| traefik | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| nginx | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

---

## Tier 2: Databases & Storage

| Image | Base | C001 | C002 | C003 | C004 | C005 | C006 | C007 | C008 | C009 | C010 | C011 | C012 | C013 | Score |
|------|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|-------|
| postgres | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| redis | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

---

## Tier 3: Security & Identity

| Image | Base | C001 | C002 | C003 | C004 | C005 | C006 | C007 | C008 | C009 | C010 | C011 | C012 | C013 | Score |
|------|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|-------|
| vault | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| keycloak | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

---

## Tier 4: Observability

| Image | Base | C001 | C002 | C003 | C004 | C005 | C006 | C007 | C008 | C009 | C010 | C011 | C012 | C013 | Score |
|------|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|-------|
| prometheus | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| loki | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |
| grafana | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

---

## Tier 5: Development & Collaboration

| Image | Base | C001 | C002 | C003 | C004 | C005 | C006 | C007 | C008 | C009 | C010 | C011 | C012 | C013 | Score |
|------|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|-------|
| forgejo | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | 🔍 | - |

---

## Hardened Image Sources (Pre-Discovery)

Before building, check these existing hardened sources:

| Source | URL | Notes |
|--------|-----|-------|
| Google Distroless | gcr.io/distroless/* | Official, trusted |
| Chainguard Images | cgr.dev/chainguard/* | Latest, actively maintained |
| Wolfi | cgr.dev/distroless/cc | Minimal base |
| NVIDIA NGC | ngc.nvidia.com/containers/* | GPU workloads |
| AWS ECR | public.ecr.aws/*/distroless-* | AWS official |

---

## Round 2 Items

Items not achievable in Round 1:

| Image | Constraint | Gap | Round 2 Action |
|-------|-----------|-----|--------------|
| TBD | C005 | Find static build or compile |
| TBD | C010 | Add wrapper script |
| TBD | C011 | Fork/fix signals |

---

## Document Control

| Version | Date | Author | Changes |
|----------|------|--------|---------|
| 1.0.0 | 2026-04-19 | Nexus | Initial |

**END OF CONSTRAINT CHECKLIST**