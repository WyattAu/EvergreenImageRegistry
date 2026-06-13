# health-shim

Tiny HTTP health probe server for database images that lack native HTTP endpoints.

## Purpose

Database images (PostgreSQL, Redis, MariaDB, MongoDB, Valkey, Kafka, etc.) don't have
native HTTP health check endpoints. This binary wraps their CLI health check commands
and exposes K8s-native HTTP probes on port 9101.

## Endpoints

| Endpoint  | Purpose                     | Response            |
|-----------|----------------------------|---------------------|
| `/livez`  | Liveness — process is alive | 200 OK / 503 Error  |
| `/readyz` | Readiness — accepting traffic| 200 OK / 503 Error  |
| `/startupz`| Startup — initialized       | 200 OK / 503 Error  |
| `/metrics`| Prometheus metrics          | text/plain          |

## Build

```bash
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o shim-amd64 .
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -ldflags="-s -w" -o shim-arm64 .
```

Binary size: ~2MB statically compiled.

## Usage

```dockerfile
ENV HEALTH_CMD="pg_isready -h localhost"
ENV READY_CMD="pg_isready -h localhost -q"
ENV STARTUP_CMD="pg_isready -h localhost"
ENV HEALTH_TIMEOUT="5"
ENV STARTUP_WINDOW="30"
ENV EVERGREEN_LOG_LEVEL="info"

COPY --from=build /build/shim /usr/local/bin/shim

# Entrypoint runs both health-shim and the database
# Runtime --init flag handles PID 1 signal handling
ENTRYPOINT ["sh", "-c", "shim & exec docker-entrypoint.sh postgres"]
```

## Environment Variables

| Variable        | Required | Default | Description                                      |
|----------------|----------|---------|--------------------------------------------------|
| `HEALTH_CMD`   | YES      | —       | CLI command for liveness check                   |
| `READY_CMD`    | NO       | HEALTH_CMD | CLI command for readiness check                |
| `STARTUP_CMD`  | NO       | HEALTH_CMD | CLI command for startup check                  |
| `LISTEN`       | NO       | :9101   | Listen address                                   |
| `HEALTH_TIMEOUT`| NO      | 5       | Timeout per check in seconds                     |
| `STARTUP_WINDOW`| NO      | 30      | Seconds after start during which startupz runs   |
| `EVERGREEN_LOG_LEVEL` | NO | info   | Log level: debug, info, warn, error              |

## Database-Specific Commands

| Database    | HEALTH_CMD                                      | READY_CMD                                       |
|-------------|------------------------------------------------|-------------------------------------------------|
| PostgreSQL  | `pg_isready -h localhost`                       | `pg_isready -h localhost -q`                    |
| Redis       | `redis-cli -h localhost ping`                   | `redis-cli -h localhost ping`                   |
| MariaDB     | `mariadb-admin ping -h 127.0.0.1 --silent`      | `mariadb-admin ping -h 127.0.0.1 --silent`      |
| MySQL       | `mariadb-admin ping -h 127.0.0.1 --silent`      | `mariadb-admin ping -h 127.0.0.1 --silent`      |
| MongoDB     | `mongosh --eval "db.adminCommand('ping')"`      | `mongosh --eval "db.adminCommand('ping')"`      |
| Valkey      | `valkey-cli -h localhost ping`                  | `valkey-cli -h localhost ping`                  |
| Kafka       | `kafka-broker-api-versions.sh --bootstrap-server localhost:9092` | same |
| RabbitMQ    | `rabbitmq-diagnostics -q ping`                  | `rabbitmq-diagnostics -q check_running`         |
| Elasticsearch| `curl -sf http://localhost:9200/_cluster/health` | same |
| Cassandra   | `nodetool status`                               | `nodetool netstats`                             |
| CouchDB     | `curl -sf http://localhost:5984/_up`            | same                                            |

## Prometheus Metrics

```
health_shim_up 1
health_shim_uptime_seconds 3600
health_shim_startup_completed 1
health_shim_info{health_cmd="pg_isready",ready_cmd="pg_isready",startup_cmd="pg_isready"} 1
```

## Integration with ADR-006

This binary implements the health shim pattern described in ADR-006 (Observability Architecture).
It runs as PID > 1 alongside the database process. The container uses `docker run --init`
or K8s `shareProcessNamespace: true` for proper PID 1 signal handling.
