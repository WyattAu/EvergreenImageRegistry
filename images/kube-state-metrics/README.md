# Kube state metrics

Kube-state-metrics - metrics about Kubernetes objects

| Attribute | Value |
|-----------|-------|
| Version | 2.18.0 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/kube-state-metrics:2.18.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
