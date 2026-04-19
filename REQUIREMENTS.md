# Sovereign Hardened Image Registry - Requirements & Constraints

**Mission:** Industrial-grade hardening image registry with 1000+ images for critical infrastructure  
**Standard:** Sovereign Hardened Image Registry v3.0.0  
**Classification:** OPERATIONAL SECURITY - ZERO-TRUST  
**Last Updated:** 2026-04-19

---

## 1. BASE IMAGE PRIORITY (MANDATORY)

The following priority order MUST be followed for ALL images:

| Priority | Base Image | Use Case | CVE Tolerance |
|----------|------------|----------|---------------|
| **1 (BEST)** | `scratch` | Static binaries only | 0 Critical/High |
| **2** | `distroless` | Minimal glibc needed | 0 Critical/High |
| **3** | `wolfi` | Package manager required | 0 Critical |
| **4 (FALLBACK)** | `debian-slim` | Legacy compatibility | 0 Critical |

### CRITICAL RULE: NEVER USE ALPINE

- Alpine Linux is **NEVER** to be used for any image
- Use Chainguard Wolfi instead: `cgr.dev/chainguard/wolfi-base:latest`
- Wolfi registry (cgr.dev) may have auth issues - use chainguard/wolfi-base as fallback

### Version Management

- All base images must use specific tags (not `latest`)
- Example: `debian:bookworm-slim`, not `debian:latest`
- Verify all download URLs are current before building

---

## 2. SECURITY CONSTRAINTS (C001-C020)

All images MUST pass these security constraints:

### CRITICAL (Must Pass)

| ID | Constraint | Description | Verification |
|----|------------|-------------|---------------|
| **C001** | Non-root execution | UID 65534 (nobody) or non-zero | `docker run --rm $IMG id -u` |
| **C002** | Read-only root filesystem | Cannot write to root at runtime | `docker run --rm --read-only $IMG touch /test` |
| **C003** | No shell | /bin/sh, /bin/bash removed | `docker run --rm $IMG test -f /bin/sh` |
| **C004** | No package manager | apt, apk, dnf, yum removed | Check for `/usr/bin/apt`, `/usr/bin/apk`, etc. |
| **C007** | Zero CVEs | 0 Critical/High vulnerabilities | Trivy scan with `CRITICAL,HIGH` |
| **C008** | Image signed | Cosign verification required | `cosign verify $IMG` |
| **C012** | No embedded secrets | No hardcoded credentials | Secret scanning |

### HIGH (Required)

| ID | Constraint | Description | Verification |
|----|------------|-------------|---------------|
| **C005** | Static linking preferred | Use `ldd` to check | Static binary preferred |
| **C006** | Stripped symbols | No debug symbols | `nm` shows minimal |
| **C009** | SBOM generated | Syft output required | `syft $IMG -o json` |
| **C010** | Health check | Working health endpoint | HTTP check |
| **C013** | OCI compliant | Image spec v1.0+ | Manifest check |
| **C014** | Minimal packages | <50 packages for non-scratch | Package count |
| **C015** | No debug tools | gdb, strace, etc. removed | Binary check |

### MEDIUM (Recommended)

| ID | Constraint | Description | Verification |
|----|------------|-------------|---------------|
| **C011** | Signal handling | SIGTERM graceful shutdown | Kill test |
| **C016** | No init system | App runs as PID 1 | Process check |
| **C017** | No Docker socket | No /var/run/docker.sock | File check |
| **C018** | No sudo/su | No privilege escalation | File check |
| **C019** | Immutable tags | Tags never overwritten | Policy |
| **C020** | User namespace isolation | Optional隔离 | Check user |

---

## 3. FUNCTIONAL TEST REQUIREMENTS

### Per-Image Test Scripts (MANDATORY)

Each image MUST have a corresponding test script that verifies:

1. **Binary execution** - Binary responds to `--version` or `--help`
2. **Health check** - Service responds on expected port
3. **Configuration** - Default config is valid
4. **Dependencies** - All required libs present

### Test Framework Location

```
images/tests/
├── test_framework.sh      # Core test utilities (C001-C020)
├── test_runner.sh        # Per-image test runner
└── test_config.yaml      # Per-image test configurations
```

### CI Integration

Tests MUST run in CI pipeline after successful build:
- Constraint tests (C001-C020)
- Functional tests (binary execution, health)
- Security tests (CVE scanning, secret detection)

---

## 4. SCALING REQUIREMENTS (1000+ IMAGES)

### Current State

- **Images Required:** 1000+ from `requiredimages.md`
- **Images Generated:** ~62 directories, ~33 with proper Dockerfiles
- **Build Status:** Failing (URL issues, Alpine usage, package availability)

### Scaling Strategy

#### Phase 1: Fix Current Builds (Current)
- [x] Fix traefik URL (3.1.4 → 3.6.13)
- [x] Fix forgejo (Debian → Wolfi base)
- [ ] Verify builds pass for ~33 images
- [ ] Integrate test scripts into CI

#### Phase 2: Expand Coverage (100 images)
- Add networking images (traefik, nginx, haproxy, envoy, etc.)
- Add database images (postgres, mysql, redis, etc.)
- Add security images (vault, keycloak, etc.)
- Verify all download URLs are current

#### Phase 3: Full Scale (1000+ images)
- Expand generator to cover all categories from `requiredimages.md`
- Add automated URL validation
- Add parallel build capability
- Implement build queue/priority system

### Category Coverage Target

| Category | Target Count | Priority |
|----------|--------------|----------|
| Networking & Gateways | 100 | CRITICAL |
| Databases & Storage | 200 | CRITICAL |
| Security & Identity | 80 | HIGH |
| Observability | 80 | HIGH |
| DevOps & CI/CD | 100 | HIGH |
| Messaging | 50 | MEDIUM |
| Git & Collaboration | 35 | MEDIUM |
| Specialized | 455 | LOW |

---

## 5. DOWNLOAD URL VERIFICATION

### Before Building ANY Image

1. Verify release exists at URL
2. Check file format (tar.gz, zip, binary)
3. Verify checksum available
4. Test URL accessibility

### Known Issue: URL Patterns Change

Examples of URL patterns that change:
- Traefik: `traefik_v{VERSION}` requires `v` prefix
- Nginx: Direct tarball, not always available
- HashiCorp: ZIP format, not tar.gz

### Automated Validation

All generators MUST include URL validation:
```python
def validate_url(url, version):
    response = requests.head(url, timeout=10)
    return response.status_code == 200
```

---

## 6. CI/CD PIPELINE REQUIREMENTS

### Pipeline Stages (IN ORDER)

1. **Discovery** - Find all Dockerfiles
2. **Lint** - Hadolint validation
3. **Build** - Multi-arch Docker build
4. **Constraint Test** - C001-C020 verification
5. **Functional Test** - Per-image tests
6. **Security Scan** - Trivy + Grype CVE scan
7. **SBOM** - Syft generation
8. **Sign** - Cosign verification
9. **Push** - GHCR.io push

### Must Pass Requirements

- All constraint tests (C001-C020)
- Zero Critical/High CVEs
- Health check passes
- Image signed

### Artifact Requirements

- SBOM in SPDX format
- Cosign signature
- Build logs with timing
- Test results

---

## 7. COMPLIANCE VERIFICATION CHECKLIST

### Pre-Build Checklist

- [ ] Base image follows priority: scratch > distroless > wolfi > debian-slim
- [ ] Alpine NEVER used
- [ ] Download URL verified current
- [ ] Version matches specification
- [ ] User created (UID 65534)
- [ ] Shell removed after user creation
- [ ] Package manager removed
- [ ] HEALTHCHECK defined
- [ ] Labels applied (vendor, version, tier)

### Post-Build Checklist

- [ ] C001: Non-root (UID != 0)
- [ ] C002: Read-only filesystem works
- [ ] C003: No shell present
- [ ] C004: No package manager
- [ ] C007: Zero Critical/High CVEs
- [ ] C008: Image signed
- [ ] C009: SBOM generated
- [ ] C010: Health check works
- [ ] C012: No embedded secrets
- [ ] C013: OCI compliant

---

## 8. FAILURE HANDLING

### Build Failures

| Failure Type | Action |
|--------------|--------|
| URL 404 | Update version, verify new URL exists |
| Package not found | Switch to direct binary download |
| Alpine base detected | Replace with wolfi or debian-slim |
| Constraint failure | Fix Dockerfile, rebuild |
| CVE failure | Update base image version |

### Known Issues Registry

Document all known issues with workarounds:
- Traefik 3.1.4 unavailable → Use 3.6.13
- Forgejo not in Debian → Use Wolfi base with binary
- Wolfi cgr.dev auth issues → Use chainguard/wolfi-base

---

## 9. DOCUMENT CONTROL

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-19 | Nexus | Initial constraint checklist |
| 2.0.0 | 2026-04-19 | Nexus | Added base image priority, scaling requirements |
| 3.0.0 | 2026-04-19 | Nexus | Added test requirements, CI pipeline specs |

---

## 10. REFERENCES

- `requiredimages.md` - Full image list (1000+)
- `generate_templates.py` - Dockerfile generator
- `extended_generator.py` - Expanded image generator
- `images/CONSTRAINT_CHECKLIST.md` - Per-image compliance matrix
- `.github/workflows/build.yml` - CI/CD pipeline

---

**END OF REQUIREMENTS DOCUMENT**
**Classification: OPERATIONAL SECURITY**