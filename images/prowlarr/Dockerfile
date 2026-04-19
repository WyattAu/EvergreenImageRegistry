# =============================================================================
# SOVEREIGN HARDENED PROWLARR
# Generated from template - Version: 1.26.0
# Constraint: official - Use official LinuxServer.io base
# =============================================================================

ARG VERSION=1.26.0
ARG BUILD_DATE

FROM lscr.io/linuxserver/prowlarr:${VERSION}

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
USER abc

WORKDIR /config
EXPOSE 9696

LABEL org.opencontainers.image.title="prowlarr" \
      org.opencontainers.image.version="1.26.0" \
      org.opencontainers.image.vendor="Prowlarr" \
      org.opencontainers.image.source="https://github.com/Prowlarr/Prowlarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"