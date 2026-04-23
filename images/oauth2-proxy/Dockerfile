# =============================================================================
# SOVEREIGN HARDENED OAUTH2-PROXY
# Generated from template - Version: 7.15.2
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=7.15.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v7.15.2/oauth2-proxy-v7.15.2.linux-amd64-sha256sum.txt" -o /oauth2-proxy.tar.gz && \
    tar -xzf /oauth2-proxy.tar.gz -C / && rm /oauth2-proxy.tar.gz && chmod +x /oauth2-proxy 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v7.15.2/oauth2-proxy-v7.15.2.linux-amd64-sha256sum.txt" -o /oauth2-proxy && chmod +x /oauth2-proxy

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/oauth2-proxy /var/cache/oauth2-proxy

FROM scratch
COPY --from=downloader /oauth2-proxy /oauth2-proxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/oauth2-proxy /var/log/oauth2-proxy
COPY --from=builder /var/cache/oauth2-proxy /var/cache/oauth2-proxy
USER 65532:65532
WORKDIR /app
EXPOSE 80 443
ENTRYPOINT ["/oauth2-proxy"]
LABEL org.opencontainers.image.title="oauth2-proxy" \
      org.opencontainers.image.version="7.15.2" \
      org.opencontainers.image.vendor="OAuth2" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM