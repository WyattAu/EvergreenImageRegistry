# Promtail

Evergreen hardened Promtail - log collection agent for Grafana Loki

| Attribute | Value |
|-----------|-------|
| Version | 2.9.4 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/promtail:2.9.4
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
