# =============================================================================
# SOVEREIGN HARDENED CONSUL
# Generated from template - Version: 1.18.1
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=1.18.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:1.18.1
RUN apk add --no-cache consul ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 consul 2>/dev/null || true
RUN mkdir -p /app /var/log/consul /var/cache/consul && chown -R consul:consul /app /var/log/consul /var/cache/consul 2>/dev/null || true
USER consul:consul
WORKDIR /app
EXPOSE 8500
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD consul members
ENTRYPOINT ["consul"]
LABEL org.opencontainers.image.title="consul" \
      org.opencontainers.image.version="1.18.1" \
      org.opencontainers.image.vendor="HashiCorp" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
