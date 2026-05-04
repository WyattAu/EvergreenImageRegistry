# Rust static

Rust static compilation base image with Rust toolchain for x86_64

| Attribute | Value |
|-----------|-------|
| Version | 1.78.0 |
| Tier | 3 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | none |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/rust-static:1.78.0
```

## Security

- Non-root by default
- HEALTHCHECK disabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
