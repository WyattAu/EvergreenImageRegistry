# =============================================================================
# SOVEREIGN HARDENED PROWLARR
# Generated from template - Version: latest
# Constraint: official - Use official LinuxServer.io base
# =============================================================================

ARG VERSION=latest
ARG BUILD_DATE


FROM lscr.io/linuxserver/prowlarr:${VERSION}
ARG VERSION=latest

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65532 -g '' app 2>/dev/null || true
USER abc
WORKDIR /config
EXPOSE 9696

LABEL org.opencontainers.image.title="prowlarr" \
      org.opencontainers.image.version="latest" \
      org.opencontainers.image.vendor="Prowlarr" \
      org.opencontainers.image.source="https://github.com/Prowlarr/Prowlarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"

LABEL sovereign.base.image="unrecognized"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM