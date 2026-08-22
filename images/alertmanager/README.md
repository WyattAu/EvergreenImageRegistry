# Alertmanager

Alertmanager - handles alerts sent by Prometheus

| Attribute | Value |
|-----------|-------|
| Version | 0.32.1 |
| Tier | 1 |
| Base Image | scratch |
| Architecture | multi-arch |
| Health Check | exec |
| SBOM | [sbom.spdx.json](sbom.spdx.json) |

## Usage

```bash
docker pull ghcr.io/wyattau/evergreenimageregistry/alertmanager:0.32.1
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

### alertmanager.yml Reference

```yaml
global:
  resolve_timeout: 5m
route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'default'
receivers:
  - name: 'default'
    webhook_configs:
      - url: 'http://localhost:9095/'
```
