# =============================================================================
# SOVEREIGN HARDENED NETCLIENT
# Generated from template - Version: 0.24.0
# Netmaker network client (static Go binary)
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.24.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/gravitl/netmaker/releases/download/v0.24.0/netclient-linux-amd64" -o /netclient && \
    strip --strip-all /netclient && \
    chmod +x /netclient

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app

FROM scratch
COPY --from=downloader /netclient /netclient
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65534:65534
WORKDIR /app
EXPOSE 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/netclient", "--version"]
ENTRYPOINT ["/netclient"]
LABEL org.opencontainers.image.title="netclient" \
      org.opencontainers.image.version="0.24.0" \
      org.opencontainers.image.vendor="Gravitl" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
