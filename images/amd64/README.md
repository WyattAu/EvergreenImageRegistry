# Amd64

Evergreen hardened amd64 - AMD64 architecture base image

| Attribute | Value |
|-----------|-------|
| Version | unknown |
| Tier | 3 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | none |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/amd64:unknown
```

## Security

- Non-root by default
- HEALTHCHECK disabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
