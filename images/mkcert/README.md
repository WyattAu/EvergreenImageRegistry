# mkcert

mkcert - Evergreen hardened image

## Quick Start

```bash
docker pull ghcr.io/wyattau/mkcert:latest
docker run -d -p 8080:8080 ghcr.io/wyattau/mkcert:latest
```

## Details

- **Tier:** standard
- **Version:** 1.4.4
- **Base:** `scratch`
- **Health Check:** Yes

## Security

- Non-root user (UID 65532)
- Distroless/wolfi-base final stage
- Multi-stage build
- SBOM included (SPDX 2.3)
