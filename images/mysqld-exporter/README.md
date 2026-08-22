# mysqld-exporter

mysqld-exporter - Evergreen hardened image

## Quick Start

```bash
docker pull ghcr.io/wyattau/mysqld-exporter:latest
docker run -d -p 8080:8080 ghcr.io/wyattau/mysqld-exporter:latest
```

## Details

- **Tier:** standard
- **Version:** latest
- **Base:** `prom/mysqld-exporter:v0.19.0`
- **Health Check:** Yes

## Security

- Non-root user (UID 65532)
- Distroless/wolfi-base final stage
- Multi-stage build
- SBOM included (SPDX 2.3)
