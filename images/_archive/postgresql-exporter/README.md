# Postgresql exporter

postgresql-exporter container image

| Attribute | Value |
|-----------|-------|
| Version | 0.15.0 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/postgresql-exporter:0.15.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
