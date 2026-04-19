# =============================================================================
# SOVEREIGN HARDENED APACHE
# Generated from template - Version: 2.4.61
# =============================================================================

ARG VERSION=2.4.61
ARG BUILD_DATE

# Apache requires compilation from source or official image
# Using official image with hardening applied
FROM httpd:2.4.61
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/httpd /var/cache/httpd && chown -R app:app /app /var/log/httpd /var/cache/httpd
USER app
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -s http://localhost:80/ || exit 1
ENTRYPOINT ["httpd", "-DFOREGROUND"]
LABEL org.opencontainers.image.title="apache" \
      org.opencontainers.image.version="2.4.61" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"