# Snmp exporter

Standalone Prometheus SNMP exporter (v0.26.0, separate from prometheus-snmp-exporter)

| Attribute | Value |
|-----------|-------|
| Version | 0.26.0 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/snmp-exporter:0.26.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
