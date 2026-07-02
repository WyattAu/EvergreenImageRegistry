# K3d

Evergreen hardened k3d - K3s in Docker

| Attribute | Value |
|-----------|-------|
| Version | 5.8.3 |
| Tier | 3 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/k3d:5.8.3
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
