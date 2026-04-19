# =============================================================================
# SOVEREIGN HARDENED VICTORIAMETRICS
# Generated from template - Version: 1.103.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=1.103.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:1.103.0
RUN apk add --no-cache victoria-metrics ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 victoria 2>/dev/null || true
RUN mkdir -p /app /var/log/victoriametrics /var/cache/victoriametrics && chown -R victoria:victoria /app /var/log/victoriametrics /var/cache/victoriametrics 2>/dev/null || true
USER victoria:victoria
WORKDIR /app
EXPOSE 8428
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /health
ENTRYPOINT ["victoria-metrics"]
LABEL org.opencontainers.image.title="victoriametrics" \
      org.opencontainers.image.version="1.103.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
