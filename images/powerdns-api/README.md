# Powerdns api

PowerDNS Authoritative Server with REST API

| Attribute | Value |
|-----------|-------|
| Version | 4.9.6 |
| Tier | 1 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/powerdns-api:4.9.6
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
