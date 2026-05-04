# Dnsmasq full

dnsmasq with full feature set (DNS, DHCP, TFTP, PXE, DNSSEC)

| Attribute | Value |
|-----------|-------|
| Version | 2.90 |
| Tier | 1 |
| Base Image | cgr.dev/chainguard/wolfi-base:latest |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/dnsmasq-full:2.90
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
