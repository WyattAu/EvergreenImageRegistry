# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS
# Generated from template - Version: 2.53.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=2.53.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:2.53.0
RUN apk add --no-cache prometheus ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 prometheus 2>/dev/null || true
RUN mkdir -p /app /var/log/prometheus /var/cache/prometheus && chown -R prometheus:prometheus /app /var/log/prometheus /var/cache/prometheus 2>/dev/null || true
USER prometheus:prometheus
WORKDIR /app
EXPOSE 9090
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /-/healthy
ENTRYPOINT ["prometheus"]
LABEL org.opencontainers.image.title="prometheus" \
      org.opencontainers.image.version="2.53.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
