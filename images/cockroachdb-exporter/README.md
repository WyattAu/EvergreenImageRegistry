# Cockroachdb exporter

CockroachDB Exporter - Prometheus exporter for CockroachDB

| Attribute | Value |
|-----------|-------|
| Version | 24.3.3 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/cockroachdb-exporter:24.3.3
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
