# ttyd

ttyd - Evergreen hardened image

## Quick Start

```bash
docker pull ghcr.io/wyattau/ttyd:latest
docker run -d -p 8080:8080 ghcr.io/wyattau/ttyd:latest
```

## Details

- **Tier:** standard
- **Version:** 1.7.7
- **Base:** `scratch`
- **Health Check:** Yes

## Security

- Non-root user (UID 65532)
- Distroless/wolfi-base final stage
- Multi-stage build
- SBOM included (SPDX 2.3)
