# Scratch go

Go source-build reference — static binary on scratch

| Attribute | Value |
|-----------|-------|
| Version | ARG |
| Tier | 0 |
| Base Image | scratch |
| Architecture | amd64 |
| Health Check | disabled |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/scratch-go:ARG
```

## Security

- Non-root by default
- HEALTHCHECK disabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
