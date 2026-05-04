# Mongodb opsmanager

MongoDB Ops Manager - mongosh CLI tool for MongoDB administration

| Attribute | Value |
|-----------|-------|
| Version | 2.5.0 |
| Tier | 2 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | tcp |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/mongodb-opsmanager:2.5.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
