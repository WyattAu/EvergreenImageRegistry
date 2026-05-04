# Maddy

Maddy - composable all-in-one mail server written in Go

| Attribute | Value |
|-----------|-------|
| Version | 0.9.3 |
| Tier | 2 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | tcp |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/maddy:0.9.3
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
