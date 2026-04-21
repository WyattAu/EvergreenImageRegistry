# =============================================================================
# SOVEREIGN HARDENED DEX
# Generated from template - Version: 2.45.1
# Constraint: scratch - built from Go source (no pre-built binaries)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.45.1
ARG BUILD_DATE

FROM golang:1.22-bookworm AS builder
RUN go install github.com/dexidp/dex/cmd/dex@latest

FROM debian:bookworm-slim AS helper
RUN mkdir -p /app /var/log/dex /var/cache/dex

FROM scratch
COPY --from=builder /go/bin/dex /dex
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=helper /app /app
COPY --from=helper /var/log/dex /var/log/dex
COPY --from=helper /var/cache/dex /var/cache/dex
USER 65534:65534
WORKDIR /app
EXPOSE 5556
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/dex", "version"]
ENTRYPOINT ["/dex"]
LABEL org.opencontainers.image.title="dex" \
      org.opencontainers.image.version="2.45.1" \
      org.opencontainers.image.vendor="Dex" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
