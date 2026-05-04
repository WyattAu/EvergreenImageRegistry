# Grafana operator

Grafana Operator - manages Grafana instances on Kubernetes

| Attribute | Value |
|-----------|-------|
| Version | 5.22.2 |
| Tier | 3 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/grafana-operator:5.22.2
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
