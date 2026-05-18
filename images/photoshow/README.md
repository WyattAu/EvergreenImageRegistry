# Photoshow

PhotoShow - PHP gallery for browsing and sharing photos

| Attribute | Value |
|-----------|-------|
| Version | v2 |
| Tier | 3 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/photoshow:v2
docker run --rm -p 8080:8080 -v /path/to/photos:/app/photos ghcr.io/wyattau/evergreenimageregistry/photoshow:v2
```

## Notes

- Uses PHP built-in development server
- Source: https://github.com/thibaud-rohmer/PhotoShow
- For production use, place behind a reverse proxy (nginx/caddy)

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
