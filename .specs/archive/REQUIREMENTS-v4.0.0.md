# Evergreen Hardened Image Registry: Unified Requirements Specification
tier-based**; it applies to every image regardless of operational tier.
| **1 (BEST)**     | `scratch`         |;                                             | none  | none            | 0 MB         | Static binary, no runtime deps              |
### 2.1 CRITICAL Constraints (BLOCKING: build fails if violated)
| **C002** | Read-only root filesystem                     | Must operate with `--read-only` flag       | `docker run --rm --read-only $IMG touch /test` must fail |;                       |
| **C004** | No package manager in final image             | apt, apk, dnf, yum must not exist          | File existence check                                     |;                       |
| **C007** | Zero Critical/High CVEs                       | 0 CVEs rated CRITICAL or HIGH              | Trivy scan                                               |;                       |
| **C008** | Image signed via Cosign                       | Signature verification must pass           | `cosign verify`                                          |;                       |
| **C012** | No embedded secrets                           | No hardcoded credentials, API keys, tokens | TruffleHog scan                                          |;                       |
### 2.2 HIGH Constraints (REQUIRED: build warns, may block)
| **C015** | No debug tools                  | gdb, strace, ltrace removed                       | Binary existence check                               |;                                               |
### 2.3 MEDIUM Constraints (RECOMMENDED: tracked, not blocking)
| **C011** | Signal handling              | Graceful SIGTERM shutdown within 10s  | Kill test                          |;                                       |
| **C019** | Immutable tags               | Tags never overwritten                | Label check: `oci.image.immutable` |;                                       |
| **C020** | Reproducible build           | Same source produces same image hash  | Build reproducibility check        |;                                       |
| **C029** | Seccomp profile compatible   | No disallowed syscalls in entrypoint  | Profile check                      |;                                       |
| **C030** | Capabilities dropped         | ALL capabilities dropped by default   | Capabilities check                 |;                                       |
| C005               |;                        | Static linking                    | C005 (restored from REQUIREMENTS.md)       |
| C006               |;                        | Stripped symbols                  | C006 (restored from REQUIREMENTS.md)       |
|;                  | C005 (old)               | No sudo/su                        | **C018** (moved to MEDIUM)                 |
|;                  | C006 (old)               | No network on startup             | **C027** (new)                             |
| C007               |;                        | Zero CVEs                         | C007 (restored from REQUIREMENTS.md)       |
| C008               |;                        | Image signed                      | C008 (restored from REQUIREMENTS.md)       |
|;                  | C007 (old)               | Minimal packages                  | **C014** (moved to HIGH)                   |
|;                  | C008 (old)               | No Docker socket                  | **C017** (moved to MEDIUM)                 |
| C009               |;                        | SBOM generated                    | C009 (restored from REQUIREMENTS.md)       |
| C010               |;                        | Health check                      | C010 (restored, now means :9101 endpoints) |
|;                  | C009 (old)               | No init system                    | **C023** (HIGH, no baked init)             |
|;                  | C010 (old)               | Health check (Docker HEALTHCHECK) | C010 (merged)                              |
|;                  | C011 (old)               | No debug tools                    | **C015** (moved to HIGH)                   |
|;                  | C012 (old)               | Immutable tags                    | **C019** (moved to MEDIUM)                 |
|;                  | C013 (old)               | Signed images                     | C008 (merged)                              |
|;                  | C014 (old)               | OCI compliance                    | **C013** (moved to HIGH)                   |
### 3.1 Port 9101: Single Observability Port
| `/metrics`  | Prometheus/OpenMetrics | 200 + text/plain metrics       |;                        |
1. **Discovery**; Find all Dockerfiles dynamically
2. **Lint**; Hadolint, ShellCheck, markdown, YAML validation
3. **Build**; Multi-arch Docker build (amd64 + arm64)
4. **Constraint Test**; C001-C030 verification via test_framework.sh
5. **Functional Test**; Per-image tests from test_config.yaml
6. **Security Scan**; Trivy + Grype CVE scanning
7. **SBOM**; Syft generation in SPDX format
8. **Sign**; Cosign signing and attestation
9. **Push**; GHCR.io push with immutable tags
**END OF UNIFIED REQUIREMENTS SPECIFICATION** **Classification: OPERATIONAL SECURITY; ZERO-TRUST** **Supersedes: