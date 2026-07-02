# Strongswan

strongSwan - IPsec-based VPN (IKEv1/IKEv2) with PKI and plugins

| Attribute | Value |
|-----------|-------|
| Version | 5.9.16 |
| Tier | 1 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | amd64 |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/strongswan:5.9.16
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
