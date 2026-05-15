# Tool Requirements and Capability Matrix

---

## Required Tools

### Build Tools

| Tool          | Min Version | Purpose            | Priority | Phase |
| ------------- | ----------- | ------------------ | -------- | ----- |
| docker        | 20.10+      | Container building | CRITICAL | -0.5  |
| docker-buildx | 0.10+       | Multi-arch builds  | CRITICAL | -0.5  |
| buildkit      | 0.11+       | Build caching      | HIGH     | -0.5  |
| kaniko        | 1.9+        | In-cluster builds  | MEDIUM   | -0.5  |

### Security Scanning Tools

| Tool  | Min Version | Purpose              | Priority | Phase |
| ----- | ----------- | -------------------- | -------- | ----- |
| trivy | 0.44+       | CVE scanning         | CRITICAL | 0     |
| grype | 0.60+       | Alternative scanning | CRITICAL | 0     |
| snyk  | 1.900+      | Commercial scanning  | HIGH     | 0     |
| clair | 4.5+        | Static analysis      | MEDIUM   | 0     |

### Supply Chain Security

| Tool   | Min Version | Purpose               | Priority | Phase |
| ------ | ----------- | --------------------- | -------- | ----- |
| cosign | 1.11+       | Image signing         | CRITICAL | 0     |
| syft   | 0.68+       | SBOM generation       | CRITICAL | 0     |
| rekor  | 0.10+       | Transparency log      | HIGH     | 0     |
| fulcio | 0.9+        | Certificate authority | HIGH     | 0     |

### Linting & Analysis

| Tool     | Min Version | Purpose            | Priority | Phase |
| -------- | ----------- | ------------------ | -------- | ----- |
| hadolint | 2.10+       | Dockerfile linting | HIGH     | 0     |
| dockle   | 0.8+        | Image security     | HIGH     | 0     |
| checkov  | 2.9+        | IaC scanning       | HIGH     | 0     |

### CI/CD Integration

| Tool           | Min Version | Purpose             | Priority | Phase |
| -------------- | ----------- | ------------------- | -------- | ----- |
| github-actions | Latest      | CI/CD               | CRITICAL | -0.5  |
| crane          | 0.12+       | Registry operations | HIGH     | -0.5  |
| helm           | 3.10+       | Package management  | HIGH     | -0.5  |

---

## Tool Installation Requirements

### Package Managers

| Platform | Package Manager | Install Command                                |
| -------- | --------------- | ---------------------------------------------- |
| Linux    | apt             | apt-get update && apt-get install -y docker.io |
| Linux    | apk             | apk add docker-cli trivy                       |
| macOS    | brew            | brew install docker trivy                      |
| Windows  | choco           | choco install docker                           |

### Binary Installation

| Tool   | Linux (amd64)        | Linux (arm64)         | macOS         |
| ------ | -------------------- | --------------------- | ------------- |
| cosign | cosign-\*.x86_64.apk | cosign-\*.aarch64.apk | cosign-\*.pkl |
| syft   | syft-\*.x86_64.apk   | syft-\*.aarch64.apk   | syft-\*.pkl   |

### Containerized Tools

All tools available as containers:

```
# Security scanning
docker run aquasec/trivy:latest trivy image <image>
docker run syft:latest syft <image>

# Supply chain
docker run sigstore/cosign:latest cosign verify <image>
```

---

## Verification Commands

### Tool Availability Verification

```bash
# Build tools
docker --version
docker buildx version

# Scanning tools
trivy --version
grype --version
syft --version

# Supply chain
cosign version

# Linting
hadolint --version
```

---

## Continuous Monitoring

| Tool   | Update Frequency | Method               |
| ------ | ---------------- | -------------------- |
| trivy  | Weekly           | trivy image --update |
| grype  | Weekly           | grype digest         |
| cosign | On-release       | GitHub releases      |
| syft   | On-release       | GitHub releases      |

---

## Capability Matrix

| Capability          | Available | Required    | Status    |
| ------------------- | --------- | ----------- | --------- |
| Docker build        | Yes       | Yes         | SATISFIED |
| Multi-arch          | Yes       | Yes         | SATISFIED |
| CVE scanning        | Yes       | Yes         | SATISFIED |
| SBOM generation     | Yes       | Yes         | SATISFIED |
| Image signing       | Yes       | Yes         | SATISFIED |
| SBOM verification   | Yes       | Yes         | SATISFIED |
| Dockerfile linting  | Yes       | Yes         | SATISFIED |
| hermetic builds     | Partial   | Yes         | GAP       |
| formal verification | No        | Conditional | GAP       |

---

## Document Control

| Version | Date       | Changes          |
| ------- | ---------- | ---------------- |
| 1.0.0   | 2026-04-19 | Initial creation |

**END OF TOOL REQUIREMENTS**
