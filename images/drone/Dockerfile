# =============================================================================
# SOVEREIGN HARDENED DRONE
# Generated from template - Version: 2.28.1
# Constraint: official - Drone complexity requires official base
# =============================================================================

ARG VERSION=2.28.1
ARG BUILD_DATE

FROM drone/drone:${VERSION}

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65534 -g '' drone 2>/dev/null || true && \
    chown -R drone:drone /data 2>/dev/null || true
USER drone

WORKDIR /data
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -s localhost:80/healthz || exit 1

LABEL org.opencontainers.image.title="drone" \
      org.opencontainers.image.version="2.28.1" \
      org.opencontainers.image.vendor="Drone" \
      org.opencontainers.image.source="https://github.com/drone/drone" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"