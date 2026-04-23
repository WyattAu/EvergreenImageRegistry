# =============================================================================
# SOVEREIGN META - OD
# This is a metadata/utility directory, not a container image.
# =============================================================================


FROM scratch
LABEL org.opencontainers.image.title="od" \
      org.opencontainers.image.description="Meta/utility directory. Not a runnable container." \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.image.category="meta" \
      sovereign.image.note="Utility directory, not a container image."

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
