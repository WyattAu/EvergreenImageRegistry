# Dendrite pot

Dendrite POT - Polylith OUTBOX Trusted worker for Dendrite

| Attribute | Value |
|-----------|-------|
| Version | 0.13.1 |
| Tier | 2 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/dendrite-pot:0.13.1
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
