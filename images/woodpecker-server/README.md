# Woodpecker server

Woodpecker Server - CI/CD server for Woodpecker CI

| Attribute | Value |
|-----------|-------|
| Version | 2.7.0 |
| Tier | 2 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/woodpecker-server:2.7.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
