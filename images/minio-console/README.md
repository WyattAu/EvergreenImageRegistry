# Minio console

MinIO Console - web-based administration UI for MinIO

| Attribute | Value |
|-----------|-------|
| Version | RELEASE.2025-10-15T17-29-55Z |
| Tier | 2 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/minio-console:RELEASE.2025-10-15T17-29-55Z
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
