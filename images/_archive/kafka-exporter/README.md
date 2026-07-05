# Kafka exporter

Kafka Exporter - Prometheus exporter for Apache Kafka

| Attribute | Value |
|-----------|-------|
| Version | 1.8.0 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/kafka-exporter:1.8.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images
