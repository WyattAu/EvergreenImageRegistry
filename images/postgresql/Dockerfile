# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL
# Generated from template - Version: 17.4
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=17.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65532 -s /usr/sbin/nologin postgres 2>/dev/null || true
RUN mkdir -p /app /var/log/postgres /var/cache/postgres

FROM golang:1.23-alpine AS health-shim-builder
COPY images/health-shim/go.mod images/health-shim/main.go /build/
RUN cd /build && CGO_ENABLED=0 go build -ldflags="-s -w" -o /health-shim .
FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
COPY --from=health-shim-builder /health-shim /usr/local/bin/health-shim
ENV HEALTH_CMD="pg_isready -h localhost" \
    READY_CMD="pg_isready -h localhost -q" \
    STARTUP_CMD="pg_isready -h localhost" \
    SOVEREIGN_LOG_LEVEL=info

RUN apk add --no-cache postgresql-17 ca-certificates
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/postgres /var/log/postgres
COPY --from=builder --chown=65532:65532 /var/cache/postgres /var/cache/postgres
USER 65532:65532
WORKDIR /app
EXPOSE 5432
ENTRYPOINT ["sh", "-c", "health-shim & exec postgres"]
LABEL org.opencontainers.image.title="postgresql" \
      org.opencontainers.image.version="17.4" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="true"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM