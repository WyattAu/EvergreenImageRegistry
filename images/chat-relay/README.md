# Chat relay

Matrix chat relay (complement) - testing tool for Matrix homeservers

| Attribute | Value |
|-----------|-------|
| Version | 0.5.0 |
| Tier | 2 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | tcp |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/chat-relay:0.5.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
