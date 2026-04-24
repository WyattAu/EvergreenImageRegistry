# =============================================================================
# SOVEREIGN HARDENED SONARR
# Generated from template - Version: 4.0.10
# Constraint: official - Use official LinuxServer.io base
# =============================================================================

ARG VERSION=4.0.10
ARG BUILD_DATE


FROM lscr.io/linuxserver/sonarr:${VERSION}
ARG VERSION=4.0.10

# Apply sovereignty hardening (already non-root in official image)
USER root
RUN useradd -m -u 65532 -g '' app 2>/dev/null || true
USER abc
WORKDIR /config
EXPOSE 8989

LABEL org.opencontainers.image.title="sonarr" \
      org.opencontainers.image.version="4.0.10" \
      org.opencontainers.image.vendor="Sonarr" \
      org.opencontainers.image.source="https://github.com/Sonarr/Sonarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"

LABEL sovereign.base.image="unrecognized"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM