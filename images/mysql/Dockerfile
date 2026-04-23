# =============================================================================
# SOVEREIGN HARDENED MYSQL
# Generated from template - Version: 8.4.1
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.4.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65532 -s /usr/sbin/nologin php84-mysql 2>/dev/null || true
RUN mkdir -p /app /var/log/mariadbd /var/cache/mariadbd

FROM go-1.23:1.23-alpine AS health-shim-builder
COPY images/health-shim/go.mod images/health-shim/main.go /build/
RUN cd /build && CGO_ENABLED=0 go build -ldflags="-s -w" -o /health-shim .
FROM cgr.dev/chainguard/wolfi-base:latest
COPY --from=health-shim-builder /health-shim /usr/local/bin/health-shim
ENV HEALTH_CMD="mariadb-admin ping -h 127.0.0.1 --silent" \
    READY_CMD="mariadb-admin ping -h 127.0.0.1 --silent" \
    STARTUP_CMD="mariadb-admin ping -h 127.0.0.1 --silent" \
    SOVEREIGN_LOG_LEVEL=info

RUN apk add --no-cache ca-certificates
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/mariadbd /var/log/mariadbd
COPY --from=builder --chown=65532:65532 /var/cache/mariadbd /var/cache/mariadbd
USER 65532:65532
WORKDIR /app
EXPOSE 3306
ENTRYPOINT ["sh", "-c", "health-shim & exec mariadbd"]
LABEL org.opencontainers.image.title="php84-mysql" \
      org.opencontainers.image.version="8.4.1" \
      org.opencontainers.image.vendor="Oracle" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="true"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM