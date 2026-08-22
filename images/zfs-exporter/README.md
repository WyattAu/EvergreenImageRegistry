# zfs-exporter

zfs-exporter - Evergreen hardened image

## Quick Start

```bash
docker pull ghcr.io/wyattau/zfs-exporter:latest
docker run -d -p 8080:8080 ghcr.io/wyattau/zfs-exporter:latest
```

## Details

- **Tier:** standard
- **Version:** latest
- **Base:** `ghcr.io/frebib/zfs-exporter:latest`
- **Health Check:** Yes

## Security

- Non-root user (UID 65532)
- Distroless/wolfi-base final stage
- Multi-stage build
- SBOM included (SPDX 2.3)
