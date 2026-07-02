# Flux image automation

Flux Image Automation Controller - automated container image updates for GitOps

| Attribute | Value |
|-----------|-------|
| Version | 1.1.2 |
| Tier | 2 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | http |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/flux-image-automation:1.1.2
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
