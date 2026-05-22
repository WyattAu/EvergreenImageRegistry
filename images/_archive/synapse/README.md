# Synapse

Synapse - Matrix homeserver for federated messaging

| Attribute | Value |
|-----------|-------|
| Version | 1.98.0 |
| Tier | 2 |
| Base Image | debian:bookworm-slim |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/synapse:1.98.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
