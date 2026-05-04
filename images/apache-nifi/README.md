# Apache nifi

Evergreen hardened Apache NiFi - data integration and flow management platform

| Attribute | Value |
|-----------|-------|
| Version | 1.26.0 |
| Tier | 1 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/apache-nifi:1.26.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
