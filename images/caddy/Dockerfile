# =============================================================================
# SOVEREIGN HARDENED CADDY
# Generated from template - Version: 2.7.6
# =============================================================================

ARG VERSION=2.7.6
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_amd64.tar.gz" -o /caddy.tar.gz && \
    tar -xzf /caddy.tar.gz -C / && rm /caddy.tar.gz && chmod +x /caddy

FROM scratch
COPY --from=downloader /caddy /caddy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /caddy && chmod +x /caddy
RUN mkdir -p /app /var/log/caddy /var/cache/caddy && chown 65534:65534 /app /var/log/caddy /var/cache/caddy
USER 65534:65534
WORKDIR /app
EXPOSE 80 443 2019
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:80//health || exit 1
ENTRYPOINT ["/caddy"]
LABEL org.opencontainers.image.title="caddy" \
      org.opencontainers.image.version="2.7.6" \
      org.opencontainers.image.vendor="Caddy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
