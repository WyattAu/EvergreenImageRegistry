# =============================================================================
# SOVEREIGN HARDENED CADDY
# Generated from template - Version: 2.7.6
# Constraint: distroless/static - no shell, no package manager
# =============================================================================

ARG VERSION=2.7.6
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_amd64.tar.gz" -o /caddy.tar.gz && \
    tar -xzf /caddy.tar.gz -C / && rm /caddy.tar.gz && chmod +x /caddy

FROM cgr.dev/chainguard/wolfi AS builder
RUN mkdir -p /app /var/log/caddy /var/cache/caddy

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /caddy /caddy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/caddy /var/log/caddy
COPY --from=builder /var/cache/caddy /var/cache/caddy
USER 65534:65534
WORKDIR /app
EXPOSE 80 443 2019
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD caddy --version 2>/dev/null || exit 1
ENTRYPOINT ["/caddy"]
LABEL org.opencontainers.image.title="caddy" \
      org.opencontainers.image.version="2.7.6" \
      org.opencontainers.image.vendor="Caddy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
