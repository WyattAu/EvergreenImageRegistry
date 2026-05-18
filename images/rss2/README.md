# RSS2 (RSS-Bridge)

RSS-Bridge - generate RSS/Atom feeds for websites that don't have them

| Attribute | Value |
|-----------|-------|
| Version | 2025-08-05 |
| Tier | 3 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/rss2:2025-08-05
docker run --rm -p 8080:8080 ghcr.io/wyattau/evergreenimageregistry/rss2:2025-08-05
```

## Notes

- Uses PHP built-in development server
- Source: https://github.com/RSS-Bridge/rss-bridge
- For production use, place behind a reverse proxy (nginx/caddy)
- Cache directory at /var/cache/rssbridge (writable)

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
