# mongodb-exporter

mongodb-exporter - Evergreen hardened image

## Quick Start

```bash
docker pull ghcr.io/wyattau/mongodb-exporter:latest
docker run -d -p 8080:8080 ghcr.io/wyattau/mongodb-exporter:latest
```

## Details

- **Tier:** standard
- **Version:** 0.51.0
- **Base:** `scratch`
- **Health Check:** Yes

## Security

- Non-root user (UID 65532)
- Distroless/wolfi-base final stage
- Multi-stage build
- SBOM included (SPDX 2.3)
