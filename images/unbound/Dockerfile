# =============================================================================
# SOVEREIGN HARDENED UNBOUND
# Generated from template - Version: 1.20.0
# =============================================================================

ARG VERSION=1.20.0
ARG BUILD_DATE

# Unbound requires compilation from source
# Using Alpine package with hardening applied
FROM alpine:3.21
RUN apk add --no-cache unbound ca-certificates && rm -rf /var/cache/apk/*
RUN adduser -D -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/unbound /var/cache/unbound && chown -R app:app /app /var/log/unbound /var/cache/unbound
USER app
WORKDIR /app
EXPOSE 53
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /usr/sbin/unbound-checkconf 2>/dev/null || exit 1
ENTRYPOINT ["/usr/sbin/unbound"]
LABEL org.opencontainers.image.title="unbound" \
      org.opencontainers.image.version="1.20.0" \
      org.opencontainers.image.vendor="NLnet Labs" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"