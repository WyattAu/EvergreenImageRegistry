# Traefik v2

Traefik v2 - modern HTTP reverse proxy and load balancer

| Attribute | Value |
|-----------|-------|
| Version | 2.11.42 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/traefik-v2:2.11.42
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
