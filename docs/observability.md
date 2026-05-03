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
| `evergreen_image_info` | gauge | Image version label |
| `evergreen_up_seconds` | gauge | Uptime in seconds |

## Dockerfile HEALTHCHECK Instruction

Every image in the registry includes a `HEALTHCHECK` instruction in its `Dockerfile`. This provides native health
status reporting to container runtimes without requiring external orchestration.

### HTTP Application Images

Images serving HTTP traffic use `curl` to check their application port:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1
```

### Database Images

Database images use their native health-check tools to validate service readiness:

| Database | HEALTHCHECK Command |
|----------|---------------------|
| PostgreSQL | `pg_isready -U $POSTGRES_USER` |
| Redis | `redis-cli ping` |
| MySQL | `mysqladmin ping -h localhost` |
| MongoDB | `mongosh --eval "db.adminCommand('ping')"` |

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD pg_isready -U $POSTGRES_USER || exit 1
```

### FROM scratch Images

Images built `FROM scratch` have no shell or utilities available, so they use `HEALTHCHECK NONE`:

```dockerfile
HEALTHCHECK NONE
```

### Metrics-Only Images

Images that exist solely to export Prometheus metrics curl their own metrics endpoint:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:9101/metrics || exit 1
```

### Images with Native Metrics
Images that already expose Prometheus metrics on port 9101 don't need the health-shim. These include:
- Prometheus exporters (node-exporter, redis-exporter, etc.)
- Go binaries with built-in metrics (consul, vault, etc.)
- Java apps with Micrometer/JMX exporters
