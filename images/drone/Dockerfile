# =============================================================================
# SOVEREIGN HARDENED DRONE
# Generated from template - Version: 2.16.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=2.16.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:2.16.0
RUN apk add --no-cache drone ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 drone 2>/dev/null || true
RUN mkdir -p /app /var/log/drone /var/cache/drone && chown -R drone:drone /app /var/log/drone /var/cache/drone 2>/dev/null || true
USER drone:drone
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /healthz
ENTRYPOINT ["drone"]
LABEL org.opencontainers.image.title="drone" \
      org.opencontainers.image.version="2.16.0" \
      org.opencontainers.image.vendor="Drone" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
