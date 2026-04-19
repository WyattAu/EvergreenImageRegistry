# =============================================================================
# SOVEREIGN HARDENED ACTIVEMQ
# Generated from template - Version: 6.1.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=6.1.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:6.1.0
RUN apk add --no-cache activemq ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 activemq 2>/dev/null || true
RUN mkdir -p /app /var/log/activemq /var/cache/activemq && chown -R activemq:activemq /app /var/log/activemq /var/cache/activemq 2>/dev/null || true
USER activemq:activemq
WORKDIR /app
EXPOSE 61616 8161
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD activemq status
ENTRYPOINT ["activemq"]
LABEL org.opencontainers.image.title="activemq" \
      org.opencontainers.image.version="6.1.0" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
