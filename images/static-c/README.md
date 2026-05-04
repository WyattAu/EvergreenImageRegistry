# Static c

Evergreen hardened static-c - Static C binary compilation base

| Attribute | Value |
|-----------|-------|
| Version | 1.0.0 |
| Tier | 3 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | none |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/static-c:1.0.0
```

## Security

- Non-root by default
- HEALTHCHECK disabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
