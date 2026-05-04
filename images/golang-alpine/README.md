# Golang alpine

Evergreen hardened go-1.23-alpine - Go build base (no Alpine, scratch)

| Attribute | Value |
|-----------|-------|
| Version | 1.22.10 |
| Tier | 3 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/golang-alpine:1.22.10
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
