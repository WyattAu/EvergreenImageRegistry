# =============================================================================
# SOVEREIGN HARDENED HAPROXY
# Generated from template - Version: 3.0.1
# =============================================================================

ARG VERSION=3.0.1
ARG BUILD_DATE

# HAProxy requires compilation or package-based installation
# Using official image with hardening applied
FROM haproxy:3.0.1-alpine
RUN apk add --no-cache ca-certificates
RUN rm -rf /var/cache/apk/*
RUN adduser -D -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/haproxy /var/cache/haproxy && chown -R app:app /app /var/log/haproxy /var/cache/haproxy
USER app
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:80/ || exit 1
ENTRYPOINT ["/usr/local/bin/haproxy", "-f", "/usr/local/etc/haproxy/haproxy.cfg"]
LABEL org.opencontainers.image.title="haproxy" \
      org.opencontainers.image.version="3.0.1" \
      org.opencontainers.image.vendor="HAProxy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"