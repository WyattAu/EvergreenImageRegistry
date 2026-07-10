# Musl

Evergreen musl-based static base for C/C++ compilation targets

| Attribute | Value |
|-----------|-------|
| Version | unknown |
| Tier | 3 |
| Base Image | cgr.dev/chainguard/static:latest |
| Architecture | amd64 |
| Health Check | none |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/musl:unknown
```

## Security

- Non-root by default
- HEALTHCHECK disabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
