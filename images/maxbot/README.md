# Maxbot

Maxbot - open source framework for creating conversational apps

| Attribute | Value |
|-----------|-------|
| Version | 0.3.0b2 |
| Tier | 3 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/maxbot:0.3.0b2
docker run --rm ghcr.io/wyattau/evergreenimageregistry/maxbot:0.3.0b2 --help
```

## Notes

- Installed via pip from PyPI
- Requires Python >= 3.9, < 3.12
- Source: https://github.com/maxbot-ai/maxbot

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
