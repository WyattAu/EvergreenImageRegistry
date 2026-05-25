# Security Policy

## Supported Versions

Evergreen Image Registry images are continuously rebuilt nightly. Only the latest version of each image is supported.

| Tag                        | Supported |
| -------------------------- | --------- |
| `latest`                   | ✅        |
| SHA-pinned (`@sha256:...`) | ✅        |
| Version tags (`vX.Y.Z`)    | ✅        |
| Older version tags         | ❌        |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, use one of these methods:

1. **GitHub Security Advisories (preferred):** Use the
   [private vulnerability reporting](https://github.com/WyattAu/EvergreenImageRegistry/security/advisories/new) feature
   to report a vulnerability.

2. **Email:** Send details to the repository maintainer. Include:
   - Description of the vulnerability
   - Affected image(s) and version(s)
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

| Action                         | Target                          |
| ------------------------------ | ------------------------------- |
| Initial acknowledgment         | Within 48 hours                 |
| Triage and severity assessment | Within 5 business days          |
| Fix or mitigation              | Depends on severity (see below) |

### Severity Levels

| Severity | Example                             | Target Fix             |
| -------- | ----------------------------------- | ---------------------- |
| Critical | RCE, auth bypass, container escape  | 24-72 hours            |
| High     | Privilege escalation, data exposure | 3-7 days               |
| Medium   | DoS, information leak               | 7-14 days              |
| Low      | Minor misconfiguration              | Next scheduled rebuild |

## Security Features

### Image Hardening

All images built by this registry include:

- **Multi-architecture support** (amd64 + arm64 for critical/standard tiers)
- **Cosign keyless signing** with GitHub OIDC (Sigstore)
- **SLSA v3 provenance attestations**
- **SBOM (Software Bill of Materials)** in SPDX format
- **Health checks** and security labels on all images
- **Digest pinning** for base images (SHA-256)

### Supply Chain Security

- **Pinned action versions:** All GitHub Actions use SHA-pinned refs
- **BuildKit secret mounts:** Tokens never leaked in build layers
- **Dependabot:** Automated dependency scanning (Docker, Cargo, Go modules, GitHub Actions)
- **Pre-push gates:** 11 quality checks before any push to main
- **SBOM drift detection:** Monitors for supply chain changes

### Vulnerability Management

- **Nightly rebuilds:** All images rebuilt daily with latest upstream patches
- **Automated version bumping:** Outdated base images detected and bumped automatically
- **SBOM attestation:** Every image includes a machine-readable software inventory

## Disclosure Policy

We practice **responsible disclosure**. Once a fix is released:

1. A GitHub Security Advisory is published
2. Affected images are rebuilt immediately
3. The advisory is submitted for CVE assignment (if applicable)
4. Credit is given to the reporter (unless anonymity is requested)

Thank you for helping keep Evergreen Image Registry and its users secure.
