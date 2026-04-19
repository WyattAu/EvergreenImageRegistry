# =============================================================================
# SOVEREIGN HARDENED HAPROXY
# Generated from template - Version: 3.0.1
# =============================================================================

ARG VERSION=3.0.1
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://www.haproxy.org/download/3.0.1/src/haproxy-3.0.1.tar.gz" -o /haproxy.tar.gz && \
    tar -xzf /haproxy.tar.gz -C / && rm /haproxy.tar.gz && chmod +x /haproxy

FROM scratch
COPY --from=downloader /haproxy /haproxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /haproxy && chmod +x /haproxy
RUN mkdir -p /app /var/log/haproxy /var/cache/haproxy && chown 65534:65534 /app /var/log/haproxy /var/cache/haproxy
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:80/stat || exit 1
ENTRYPOINT ["/haproxy"]
LABEL org.opencontainers.image.title="haproxy" \
      org.opencontainers.image.version="3.0.1" \
      org.opencontainers.image.vendor="HAProxy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
