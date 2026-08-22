# Prometheus

Prometheus - monitoring and alerting toolkit

| Attribute | Value |
|-----------|-------|
| Version | 2.53.0 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/prometheus:2.53.0
```

## Security

- Non-root by default
- HEALTHCHECK enabled
- SBOM available ([sbom.spdx.json](sbom.spdx.json))
- Digest-pinned base images

## ⚠️ Configuration Required

This image requires a configuration file to start. Without it, the container will exit immediately.

### Quick Start

```bash
# grafana: mount grafana.ini
docker run -d -p 3000:3000 \
  -v /path/to/grafana.ini:/etc/grafana/grafana.ini:ro \
  ghcr.io/wyattau/evergreenimageregistry/grafana:latest

# Example grafana.ini
cat > grafana.ini << 'CFG'
[server]
http_port = 3000
CFG
```

### prometheus.yml Reference

```yaml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
```
