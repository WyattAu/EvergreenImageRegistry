# =============================================================================
# SOVEREIGN HARDENED JELLYFIN
# Generated from template - Version: 10.10.0
# Constraint: official - Use official Jellyfin base
# =============================================================================

ARG VERSION=10.10.0
ARG BUILD_DATE

FROM jellyfin/jellyfin:${VERSION}

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65534 -g '' jellyfin 2>/dev/null || true && \
    chown -R jellyfin:jellyfin /config /cache /media 2>/dev/null || true
USER jellyfin

WORKDIR /config
EXPOSE 8096

LABEL org.opencontainers.image.title="jellyfin" \
      org.opencontainers.image.version="10.10.0" \
      org.opencontainers.image.vendor="Jellyfin" \
      org.opencontainers.image.source="https://github.com/jellyfin/jellyfin" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"