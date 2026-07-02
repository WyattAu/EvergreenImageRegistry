# Minio

MinIO - high-performance object storage compatible with S3

| Attribute | Value |
|-----------|-------|
| Version | RELEASE.2025-10-15T17-29-55Z |
| Tier | 1 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/minio:RELEASE.2025-10-15T17-29-55Z
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
