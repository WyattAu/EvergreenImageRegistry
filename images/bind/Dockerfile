# =============================================================================
# SOVEREIGN HARDENED BIND
# Generated from template - Version: 9.18.0
# =============================================================================

ARG VERSION=9.18.0
ARG BUILD_DATE

# BIND requires compilation from source or official image
# Using official image with hardening applied
FROM isc/bind:9.18.0
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/named /var/cache/bind && chown -R app:app /app /var/log/named /var/cache/bind
USER app
WORKDIR /app
EXPOSE 53 953
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /usr/sbin/named-checkconf 2>/dev/null || exit 1
ENTRYPOINT ["/usr/sbin/named", "-f", "-g"]
LABEL org.opencontainers.image.title="bind" \
      org.opencontainers.image.version="9.18.0" \
      org.opencontainers.image.vendor="ISC" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"