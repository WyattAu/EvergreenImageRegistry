# =============================================================================
# SOVEREIGN HARDENED HAPROXY
# Generated from template - Version: 3.0.1
# Constraint: distroless/static - no shell, no package manager
# =============================================================================

ARG VERSION=3.0.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://www.haproxy.org/download/3.0.1/src/haproxy-3.0.1.tar.gz" -o /haproxy.tar.gz && \
    tar -xzf /haproxy.tar.gz -C / && rm /haproxy.tar.gz && chmod +x /haproxy

FROM cgr.dev/chainguard/wolfi AS builder
RUN mkdir -p /app /var/log/haproxy /var/cache/haproxy

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /haproxy /haproxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/haproxy /var/log/haproxy
COPY --from=builder /var/cache/haproxy /var/cache/haproxy
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD haproxy --version 2>/dev/null || exit 1
ENTRYPOINT ["/haproxy"]
LABEL org.opencontainers.image.title="haproxy" \
      org.opencontainers.image.version="3.0.1" \
      org.opencontainers.image.vendor="HAProxy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
