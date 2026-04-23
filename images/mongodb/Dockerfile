# =============================================================================
# SOVEREIGN HARDENED MONGODB
# Generated from template - Version: 7.0.11
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.0.11
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65532 -s /usr/sbin/nologin mongodb 2>/dev/null || true
RUN mkdir -p /app /var/log/mongod /var/cache/mongod

FROM go-1.23:1.23-alpine AS health-shim-builder
COPY images/health-shim/go.mod images/health-shim/main.go /build/
RUN cd /build && CGO_ENABLED=0 go build -ldflags="-s -w" -o /health-shim .
FROM cgr.dev/chainguard/wolfi-base:latest
COPY --from=health-shim-builder /health-shim /usr/local/bin/health-shim
ENV HEALTH_CMD="mongosh --eval \"db.adminCommand('ping')\"" \
    READY_CMD="mongosh --eval \"db.adminCommand('ping')\"" \
    STARTUP_CMD="mongosh --eval \"db.adminCommand('ping')\"" \
    SOVEREIGN_LOG_LEVEL=info

RUN apk add --no-cache ca-certificates
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/mongod /var/log/mongod
COPY --from=builder --chown=65532:65532 /var/cache/mongod /var/cache/mongod
USER 65532:65532
WORKDIR /app
EXPOSE 27017
ENTRYPOINT ["sh", "-c", "health-shim & exec mongod"]
LABEL org.opencontainers.image.title="mongodb" \
      org.opencontainers.image.version="7.0.11" \
      org.opencontainers.image.vendor="MongoDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="true"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM