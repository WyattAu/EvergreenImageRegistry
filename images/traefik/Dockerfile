# =============================================================================
# SOVEREIGN HARDENED TRAEFIK
# Generated from template - Version: 3.1.4
# Constraint: distroless/static - no shell, no package manager
# =============================================================================

ARG VERSION=3.1.4
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://github.com/traefik/traefik/releases/download/v3.1.4/traefik_3.1.4_linux_amd64.tar.gz" -o /traefik.tar.gz && \
    tar -xzf /traefik.tar.gz -C / && rm /traefik.tar.gz && chmod +x /traefik

FROM cgr.dev/chainguard/wolfi AS builder
RUN mkdir -p /app /var/log/traefik /var/cache/traefik

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /traefik /traefik
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/traefik /var/log/traefik
COPY --from=builder /var/cache/traefik /var/cache/traefik
USER 65534:65534
WORKDIR /app
EXPOSE 80 443 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD traefik --version 2>/dev/null || exit 1
ENTRYPOINT ["/traefik"]
LABEL org.opencontainers.image.title="traefik" \
      org.opencontainers.image.version="3.1.4" \
      org.opencontainers.image.vendor="Traefik Labs" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
