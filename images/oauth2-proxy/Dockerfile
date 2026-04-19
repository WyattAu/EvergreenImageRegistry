# =============================================================================
# SOVEREIGN HARDENED OAUTH2-PROXY
# Generated from template - Version: 7.6.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=7.6.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v7.6.0/oauth2-proxy_7.6.0_linux_amd64.tar.gz" -o /oauth2-proxy.tar.gz && \
    tar -xzf /oauth2-proxy.tar.gz -C / && rm /oauth2-proxy.tar.gz && chmod +x /oauth2-proxy 2>/dev/null || \
    curl -fsSL "https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v7.6.0/oauth2-proxy_7.6.0_linux_amd64.tar.gz" -o /oauth2-proxy && chmod +x /oauth2-proxy

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/oauth2-proxy /var/cache/oauth2-proxy

FROM scratch
COPY --from=downloader /oauth2-proxy /oauth2-proxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/oauth2-proxy /var/log/oauth2-proxy
COPY --from=builder /var/cache/oauth2-proxy /var/cache/oauth2-proxy
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/oauth2-proxy", "--version"]
ENTRYPOINT ["/oauth2-proxy"]
LABEL org.opencontainers.image.title="oauth2-proxy" \
      org.opencontainers.image.version="7.6.0" \
      org.opencontainers.image.vendor="OAuth2" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
