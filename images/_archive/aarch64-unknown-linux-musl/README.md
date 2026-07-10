# Aarch64 unknown linux musl

Evergreen hardened aarch64-unknown-linux-musl - ARM64 musl static base

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
docker pull ghcr.io/wyattau/evergreenimageregistry/aarch64-unknown-linux-musl:unknown
```

## Security

- Non-root by default
- HEALTHCHECK disabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
