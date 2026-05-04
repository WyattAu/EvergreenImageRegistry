# Openjdk alpine

Evergreen hardened openjdk-alpine - JRE runtime (no Alpine, debian-slim)

| Attribute | Value |
|-----------|-------|
| Version | 21-slim |
| Tier | 3 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/openjdk-alpine:21-slim
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
