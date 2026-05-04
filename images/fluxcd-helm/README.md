# Fluxcd helm

Evergreen hardened fluxcd-helm - Helm controller for Flux

| Attribute | Value |
|-----------|-------|
| Version | 2.8.6 |
| Tier | 3 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/fluxcd-helm:2.8.6
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
