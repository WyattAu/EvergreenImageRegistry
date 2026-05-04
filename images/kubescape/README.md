# Kubescape

Kubescape - Kubernetes security platform

| Attribute | Value |
|-----------|-------|
| Version | 4.0.5 |
| Tier | 3 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/kubescape:4.0.5
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
