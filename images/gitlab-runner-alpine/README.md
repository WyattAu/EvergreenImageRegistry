# Gitlab runner alpine

GitLab Runner (scratch) - CI/CD runner for GitLab, minimal scratch image

| Attribute | Value |
|-----------|-------|
| Version | 16.11.0 |
| Tier | 2 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/gitlab-runner-alpine:16.11.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
