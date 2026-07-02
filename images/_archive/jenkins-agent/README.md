# Jenkins agent

Evergreen hardened jenkins-agent - Jenkins SSH/JNLP agent

| Attribute | Value |
|-----------|-------|
| Version | 3355.v388858a_47b_33 |
| Tier | 3 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/jenkins-agent:3355.v388858a_47b_33
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
