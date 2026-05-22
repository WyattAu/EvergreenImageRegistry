# Prometheus config

Evergreen hardened prometheus-config - Prometheus config reloader

| Attribute | Value |
|-----------|-------|
| Version | 0.90.1 |
| Tier | 3 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/prometheus-config:0.90.1
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
