# =============================================================================
# SOVEREIGN HARDENED OPENHAB
# Generated from template - Version: 4.2.0
# Constraint: official - Use official OpenHAB base
# =============================================================================

ARG VERSION=4.2.0
ARG BUILD_DATE

FROM openhab/openhab:${VERSION}

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65534 -g '' openhab 2>/dev/null || true && \
    chown -R openhab:openhab /openhab/conf /openhab/userdata 2>/dev/null || true
USER openhab

WORKDIR /openhab
EXPOSE 8080 8443

LABEL org.opencontainers.image.title="openhab" \
      org.opencontainers.image.version="4.2.0" \
      org.opencontainers.image.vendor="OpenHAB" \
      org.opencontainers.image.source="https://github.com/openhab/openhab-docker" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"