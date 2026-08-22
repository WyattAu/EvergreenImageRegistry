# restic-rest-server

restic-rest-server - Evergreen hardened image

## Quick Start

```bash
docker pull ghcr.io/wyattau/restic-rest-server:latest
docker run -d -p 8080:8080 ghcr.io/wyattau/restic-rest-server:latest
```

## Details

- **Tier:** standard
- **Version:** 0.14.0
- **Base:** `scratch`
- **Health Check:** Yes

## Security

- Non-root user (UID 65532)
- Distroless/wolfi-base final stage
- Multi-stage build
- SBOM included (SPDX 2.3)
