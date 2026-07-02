# Meilisearch

Meilisearch - fast, relevant, and typo-tolerant search engine

| Attribute | Value |
|-----------|-------|
| Version | 1.42.1 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/meilisearch:1.42.1
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
