# Observability Integration Guide

## Health Shim

The `health-shim` image provides universal health/metrics endpoints for images that don't natively support Prometheus metrics.

### Endpoints
- `/livez` — Liveness probe (always returns 200 OK)
- `/readyz` — Readiness probe (always returns 200 OK)
- `/metrics` — Prometheus metrics (image version, uptime)

### Integration Pattern

For images without native metrics, add the health-shim as a sidecar:

```yaml
# docker-compose.yml
services:
  myapp:
    image: ghcr.io/owner/myapp:latest
    # ... app config ...

  myapp-metrics:
    image: ghcr.io/owner/health-shim:latest
    environment:
      - IMAGE_VERSION=1.0.0
      - METRICS_PORT=9101
    ports:
      - "9101:9101"
```

### Metrics Available
| Metric | Type | Description |
|--------|------|-------------|
| `sovereign_image_info` | gauge | Image version label |
| `sovereign_up_seconds` | gauge | Uptime in seconds |

### Images with Native Metrics
Images that already expose Prometheus metrics on port 9101 don't need the health-shim. These include:
- Prometheus exporters (node-exporter, redis-exporter, etc.)
- Go binaries with built-in metrics (consul, vault, etc.)
- Java apps with Micrometer/JMX exporters
