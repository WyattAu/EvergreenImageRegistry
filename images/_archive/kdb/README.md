# Kdb

Placeholder for KX Systems KDB+ proprietary database. Requires license.

| Attribute | Value |
|-----------|-------|
| Version | unknown |
| Tier | 2 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | none |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/kdb:unknown
```

## Security

- Non-root by default
- HEALTHCHECK disabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
