# Argocd notifications

ArgoCD Notifications - notification controller for ArgoCD

| Attribute | Value |
|-----------|-------|
| Version | 2.12.6 |
| Tier | 2 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/argocd-notifications:2.12.6
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
