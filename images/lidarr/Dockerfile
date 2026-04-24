# =============================================================================
# SOVEREIGN HARDENED LIDARR
# Generated from template - Version: latest
# Constraint: official - Use official LinuxServer.io base
# =============================================================================

ARG VERSION=latest
ARG BUILD_DATE


FROM lscr.io/linuxserver/lidarr:${VERSION}
ARG VERSION=latest

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65532 -g '' app 2>/dev/null || true
USER abc
WORKDIR /config
EXPOSE 8686

LABEL org.opencontainers.image.title="lidarr" \
      org.opencontainers.image.version="latest" \
      org.opencontainers.image.vendor="Lidarr" \
      org.opencontainers.image.source="https://github.com/Lidarr/Lidarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"

LABEL sovereign.base.image="unrecognized"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM