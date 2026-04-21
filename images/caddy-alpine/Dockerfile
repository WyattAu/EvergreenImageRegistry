# =============================================================================
# SOVEREIGN HARDENED CADDY-ALPINE
# Caddy web server with automatic HTTPS
# Constraint: alpine - lightweight base per image name
# =============================================================================

ARG VERSION=2.8.4
ARG BUILD_DATE

FROM alpine:3.19 AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://github.com/caddyserver/caddy/releases/download/v${VERSION}/caddy_${VERSION}_linux_amd64.tar.gz" -o /caddy.tar.gz && \
    tar -xzf /caddy.tar.gz -C / && rm /caddy.tar.gz && chmod +x /caddy

FROM alpine:3.19
RUN apk add --no-cache ca-certificates libcap && \
    mkdir -p /app /var/log/caddy /var/cache/caddy /var/lib/caddy
COPY --from=downloader /caddy /usr/local/bin/caddy
RUN chown -R 65534:65534 /app /var/log/caddy /var/cache/caddy /var/lib/caddy && \
    setcap cap_net_bind_service=+ep /usr/local/bin/caddy 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 80 443 443/udp 2019
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/caddy", "version"]
ENTRYPOINT ["/usr/local/bin/caddy"]
CMD ["run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
LABEL org.opencontainers.image.title="caddy-alpine" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Caddy Server" \
      org.opencontainers.image.source="https://github.com/caddyserver/caddy" \
      org.opencontainers.image.description="Caddy web server with automatic HTTPS on Alpine Linux" \
      sovereign.image.tier="1" \
      sovereign.image.category="webserver" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="alpine" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
