# Woodpecker ci

Woodpecker CI Server - CI/CD server (woodpecker-ci is the server binary)

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
docker pull ghcr.io/wyattau/evergreenimageregistry/woodpecker-ci:2.7.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
