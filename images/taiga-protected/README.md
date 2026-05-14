# taiga-protected

Taiga Protected - file access protection proxy for Taiga

| Attribute | Value |
|-----------|-------|
| Version | 6.9.0 |
| Tier | 3 |
| Base Image | wolfi |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/taiga-protected:6.9.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
