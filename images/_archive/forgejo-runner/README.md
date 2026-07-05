# Forgejo runner

Forgejo Act Runner - CI/CD runner for Forgejo

| Attribute | Value |
|-----------|-------|
| Version | 6.3.1 |
| Tier | 2 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | tcp |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/forgejo-runner:6.3.1
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
