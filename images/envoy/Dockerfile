# =============================================================================
# SOVEREIGN HARDENED ENVOY
# Generated from template - Version: 1.31.0
# =============================================================================

ARG VERSION=1.31.0
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://envoy.io/" -o /envoy.tar.gz && \
    tar -xzf /envoy.tar.gz -C / && rm /envoy.tar.gz && chmod +x /envoy

FROM scratch
COPY --from=downloader /envoy /envoy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /envoy && chmod +x /envoy
RUN mkdir -p /app /var/log/envoy /var/cache/envoy && chown 65534:65534 /app /var/log/envoy /var/cache/envoy
USER 65534:65534
WORKDIR /app
EXPOSE 80 443 9900
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:80//ready || exit 1
ENTRYPOINT ["/envoy"]
LABEL org.opencontainers.image.title="envoy" \
      org.opencontainers.image.version="1.31.0" \
      org.opencontainers.image.vendor="Envoy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
