# Vikunja redis

Vikunja API with Redis backend configuration

| Attribute | Value |
|-----------|-------|
| Version | v0.24.1 |
| Tier | 2 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/vikunja-redis:v0.24.1
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
