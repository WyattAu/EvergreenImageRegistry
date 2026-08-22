# taiga-events

Taiga Events - real-time events service for Taiga

## Quick Start

```bash
docker pull ghcr.io/wyattau/taiga-events:latest
docker run -d -p 8080:8080 ghcr.io/wyattau/taiga-events:latest
```

## Details

- **Tier:** standard
- **Version:** 6.9.0
- **Base:** `taigaio/taiga-events`
- **Health Check:** Yes

## Security

- Non-root user (UID 65532)
- Distroless/wolfi-base final stage
- Multi-stage build
- SBOM included (SPDX 2.3)
