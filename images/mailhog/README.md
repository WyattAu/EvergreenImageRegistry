# Mailhog

MailHog - email testing tool with web UI

| Attribute | Value |
|-----------|-------|
| Version | 1.0.1 |
| Tier | 2 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | http |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/mailhog:1.0.1
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
