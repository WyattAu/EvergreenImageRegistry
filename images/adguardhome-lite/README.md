# Adguardhome lite

AdGuard Home with lite/minimal config entrypoint

| Attribute | Value |
|-----------|-------|
| Version | 0.107.50 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/adguardhome-lite:0.107.50
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
