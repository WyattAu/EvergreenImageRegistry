# =============================================================================
# SOVEREIGN HARDENED VALKEY
# Generated from template - Version: 7.2.4
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.2.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65532 -s /usr/sbin/nologin valkey 2>/dev/null || true
RUN mkdir -p /app /var/log/valkey /var/cache/valkey

FROM golang:1.23-alpine AS health-shim-builder
COPY images/health-shim/go.mod images/health-shim/main.go /build/
RUN cd /build && CGO_ENABLED=0 go build -ldflags="-s -w" -o /health-shim .
FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
COPY --from=health-shim-builder /health-shim /usr/local/bin/health-shim
ENV HEALTH_CMD="valkey-cli ping" \
    READY_CMD="valkey-cli ping" \
    STARTUP_CMD="valkey-cli ping" \
    SOVEREIGN_LOG_LEVEL=info

RUN apk add --no-cache valkey ca-certificates
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/valkey /var/log/valkey
COPY --from=builder --chown=65532:65532 /var/cache/valkey /var/cache/valkey
USER 65532:65532
WORKDIR /app
EXPOSE 6379
ENTRYPOINT ["sh", "-c", "health-shim & exec valkey"]
LABEL org.opencontainers.image.title="valkey" \
      org.opencontainers.image.version="7.2.4" \
      org.opencontainers.image.vendor="Valkey" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="true"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM