# =============================================================================
# SOVEREIGN ALIAS - JELLYFIN-SERVER -> jellyfin
# Alias for images/jellyfin/
# =============================================================================

ARG VERSION=10.10.0
ARG BUILD_DATE

FROM jellyfin/jellyfin:${VERSION}

RUN useradd -m -u 65532 -g '' jellyfin 2>/dev/null || true && \
    chown -R jellyfin:jellyfin /config /cache /media 2>/dev/null || true
USER jellyfin

WORKDIR /config
EXPOSE 8096
LABEL org.opencontainers.image.title="jellyfin-server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Jellyfin" \
      org.opencontainers.image.source="https://github.com/jellyfin/jellyfin" \
      sovereign.image.tier="2" \
      sovereign.image.status="functional" \
      sovereign.image.category="media" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"

LABEL sovereign.base.image="unrecognized"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM