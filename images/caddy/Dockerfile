# =============================================================================
# SOVEREIGN HARDENED CADDY
# Generated from template - Version: 2.7.6
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.7.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_amd64.tar.gz" -o /caddy.tar.gz && \
    tar -xzf /caddy.tar.gz -C / && rm /caddy.tar.gz && chmod +x /caddy 2>/dev/null || \
    curl -fsSL "https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_amd64.tar.gz" -o /caddy && chmod +x /caddy

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/caddy /var/cache/caddy

FROM scratch
COPY --from=downloader /caddy /caddy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/caddy /var/log/caddy
COPY --from=builder /var/cache/caddy /var/cache/caddy
USER 65534:65534
WORKDIR /app
EXPOSE 80 443 2019
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/caddy", "version"]
ENTRYPOINT ["/caddy"]
LABEL org.opencontainers.image.title="caddy" \
      org.opencontainers.image.version="2.7.6" \
      org.opencontainers.image.vendor="Caddy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
