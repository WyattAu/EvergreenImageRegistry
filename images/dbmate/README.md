# Dbmate

Database migration tool for PostgreSQL, MySQL, SQLite, CockroachDB

| Attribute | Value |
|-----------|-------|
| Version | 2.33.0 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | none |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/dbmate:2.33.0
```

## Security

- Non-root by default
- HEALTHCHECK disabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
