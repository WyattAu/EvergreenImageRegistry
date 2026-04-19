# =============================================================================
# SOVEREIGN HARDENED RADARR
# Generated from template - Version: 5.14.0
# Constraint: official - Use official LinuxServer.io base
# =============================================================================

ARG VERSION=5.14.0
ARG BUILD_DATE

FROM lscr.io/linuxserver/radarr:${VERSION}

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
USER abc

WORKDIR /config
EXPOSE 7878

LABEL org.opencontainers.image.title="radarr" \
      org.opencontainers.image.version="5.14.0" \
      org.opencontainers.image.vendor="Radarr" \
      org.opencontainers.image.source="https://github.com/Radarr/Radarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"