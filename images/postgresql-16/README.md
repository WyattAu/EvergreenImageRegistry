# postgresql-16

PostgreSQL 16 - Chainguard wolfi-base, non-root, health shim

## Quick Start

```bash
docker pull ghcr.io/wyattau/postgresql-16:latest
docker run -d -p 8080:8080 ghcr.io/wyattau/postgresql-16:latest
```

## Details

- **Tier:** critical
- **Version:** 16.4
- **Base:** `cgr.dev/chainguard/postgres:latest`
- **Health Check:** Yes

## Security

- Non-root user (UID 65532)
- Distroless/wolfi-base final stage
- Multi-stage build
- SBOM included (SPDX 2.3)
