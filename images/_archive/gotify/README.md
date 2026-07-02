# Gotify

Gotify - simple push notification server

| Attribute | Value |
|-----------|-------|
| Version | 2.9.1 |
| Tier | 2 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | http |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/gotify:2.9.1
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
