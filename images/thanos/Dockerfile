# =============================================================================
# SOVEREIGN HARDENED THANOS
# Generated from template - Version: 0.35.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=0.35.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:0.35.0
RUN apk add --no-cache thanos ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 thanos 2>/dev/null || true
RUN mkdir -p /app /var/log/thanos /var/cache/thanos && chown -R thanos:thanos /app /var/log/thanos /var/cache/thanos 2>/dev/null || true
USER thanos:thanos
WORKDIR /app
EXPOSE 10902
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /-/healthy
ENTRYPOINT ["thanos"]
LABEL org.opencontainers.image.title="thanos" \
      org.opencontainers.image.version="0.35.0" \
      org.opencontainers.image.vendor="Thanos" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
