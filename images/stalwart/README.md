# Stalwart

Stalwart Mail Server - all-in-one mail server written in Rust

| Attribute | Value |
|-----------|-------|
| Version | 0.16.2 |
| Tier | 2 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | tcp |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/stalwart:0.16.2
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
