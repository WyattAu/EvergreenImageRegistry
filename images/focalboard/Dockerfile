# =============================================================================
# SOVEREIGN REFERENCE - FOCALBOARD
# Focalboard was merged into Mattermost as the 'Boards' plugin.
# No standalone releases exist anymore.
# See: images/mattermost/
# =============================================================================


FROM scratch
LABEL org.opencontainers.image.title="focalboard" \
      org.opencontainers.image.description="DEPRECATED: Focalboard merged into Mattermost as 'Boards' plugin. See images/mattermost/." \
      org.opencontainers.image.vendor="Mattermost" \
      sovereign.image.tier="3" \
      sovereign.image.status="deprecated" \
      sovereign.image.category="collaboration" \
      sovereign.image.note="Focalboard was merged into Mattermost as the 'Boards' plugin. Use images/mattermost/ instead."

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
