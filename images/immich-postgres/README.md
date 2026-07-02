# Immich Postgres

PostgreSQL 16 with pgvector extension for Immich

| Attribute | Value |
|-----------|-------|
| Version | 16.6 |
| Tier | critical |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/immich-postgres:16.6
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
