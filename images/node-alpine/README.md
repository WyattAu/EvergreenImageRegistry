# Node alpine

Evergreen hardened node-alpine - Node.js runtime (no Alpine, scratch)

| Attribute | Value |
|-----------|-------|
| Version | 22.12.0 |
| Tier | 3 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/node-alpine:22.12.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
