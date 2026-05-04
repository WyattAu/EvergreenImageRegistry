# Modsecurity crs

Evergreen hardened ModSecurity CRS - OWASP Core Rule Set

| Attribute | Value |
|-----------|-------|
| Version | 3.3.5 |
| Tier | 1 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/modsecurity-crs:3.3.5
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
