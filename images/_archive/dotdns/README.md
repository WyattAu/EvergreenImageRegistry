# Dotdns

DotDNS - DNS-over-TLS proxy server (stub - upstream repo not found)

| Attribute | Value |
|-----------|-------|
| Version | 0.1.0 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/dotdns:0.1.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
