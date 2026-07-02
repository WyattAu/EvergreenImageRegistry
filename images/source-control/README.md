# Source control

Source control management - Gitea lightweight Git server

| Attribute | Value |
|-----------|-------|
| Version | 1.22.0 |
| Tier | 2 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | multi-arch |
| Health Check | http |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/source-control:1.22.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
