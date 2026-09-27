# minio-mc

minio-mc - Evergreen hardened image

## Quick Start

```bash
docker pull ghcr.io/wyattau/minio-mc:latest
docker run -d -p 8080:8080 ghcr.io/wyattau/minio-mc:latest
```

## Details

- **Tier:** standard
- **Version:** RELEASE.2025-08-13T08-35-41Z
- **Base:** `scratch`
- **Health Check:** Yes

## Security

- Non-root user (UID 65532)
- Distroless/wolfi-base final stage
- Multi-stage build
- SBOM included (SPDX 2.3)
