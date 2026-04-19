# =============================================================================
# SOVEREIGN HARDENED LIDARR
# Generated from template - Version: 2.5.0
# Constraint: official - Use official LinuxServer.io base
# =============================================================================

ARG VERSION=2.5.0
ARG BUILD_DATE

FROM lscr.io/linuxserver/lidarr:${VERSION}

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
USER abc

WORKDIR /config
EXPOSE 8686

LABEL org.opencontainers.image.title="lidarr" \
      org.opencontainers.image.version="2.5.0" \
      org.opencontainers.image.vendor="Lidarr" \
      org.opencontainers.image.source="https://github.com/Lidarr/Lidarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"