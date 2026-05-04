# Stalwart bitnami

Stalwart Mail Server (Bitnami variant) - all-in-one mail server

| Attribute | Value |
|-----------|-------|
| Version | 0.16.2 |
| Tier | 2 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | tcp |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/stalwart-bitnami:0.16.2
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
