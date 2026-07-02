# Minio operator

MinIO Operator - Kubernetes operator for MinIO

| Attribute | Value |
|-----------|-------|
| Version | v6.0.4 |
| Tier | 2 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/minio-operator:v6.0.4
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
