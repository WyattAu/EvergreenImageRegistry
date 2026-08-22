# frp

frp - Evergreen hardened image

## Quick Start

```bash
docker pull ghcr.io/wyattau/frp:latest
docker run -d -p 8080:8080 ghcr.io/wyattau/frp:latest
```

## Details

- **Tier:** standard
- **Version:** 0.70.0
- **Base:** `scratch`
- **Health Check:** Yes

## Security

- Non-root user (UID 65532)
- Distroless/wolfi-base final stage
- Multi-stage build
- SBOM included (SPDX 2.3)
