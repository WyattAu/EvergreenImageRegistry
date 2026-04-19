# =============================================================================
# SOVEREIGN HARDENED TRAEFIK
# Generated from template - Version: 3.1.4
# =============================================================================

ARG VERSION=3.1.4
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://github.com/traefik/traefik/releases/download/v3.1.4/traefik_v3.1.4_linux_amd64.tar.gz" -o /traefik.tar.gz && \
    tar -xzf /traefik.tar.gz -C / && rm /traefik.tar.gz && chmod +x /traefik

FROM scratch
COPY --from=downloader /traefik /traefik
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app /var/log/traefik /var/cache/traefik
USER 65534:65534
WORKDIR /app
EXPOSE 80 443 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:80//ping || exit 1
ENTRYPOINT ["/traefik"]
LABEL org.opencontainers.image.title="traefik" \
      org.opencontainers.image.version="3.1.4" \
      org.opencontainers.image.vendor="Traefik Labs" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
