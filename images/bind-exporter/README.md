# bind-exporter

BIND exporter for Prometheus

## Quick Start

```bash
docker pull ghcr.io/wyattau/bind-exporter:latest
docker run -d -p 8080:8080 ghcr.io/wyattau/bind-exporter:latest
```

## Details

- **Tier:** standard
- **Version:** latest
- **Base:** `scratch`
- **Health Check:** Yes

## Security

- Non-root user (UID 65532)
- Distroless/wolfi-base final stage
- Multi-stage build
- SBOM included (SPDX 2.3)
