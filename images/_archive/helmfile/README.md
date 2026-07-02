# Helmfile

helmfile container image

| Attribute | Value |
|-----------|-------|
| Version | 0.162.0 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/helmfile:0.162.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
