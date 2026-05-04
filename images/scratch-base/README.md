# Scratch base

Minimal FROM scratch base with CA certs, tzdata, and standard directories

| Attribute | Value |
|-----------|-------|
| Version | unknown |
| Tier | 0 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | disabled |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/scratch-base:unknown
```

## Security

- Non-root by default
- HEALTHCHECK disabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
