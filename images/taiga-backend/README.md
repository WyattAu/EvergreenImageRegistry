# Taiga backend

taiga-backend container image

| Attribute | Value |
|-----------|-------|
| Version | 6.8.2 |
| Tier | unknown |
| Base Image | debian:bookworm-slim |
| Architecture | amd64 |
| Health Check | enabled |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/taiga-backend:6.8.2
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
