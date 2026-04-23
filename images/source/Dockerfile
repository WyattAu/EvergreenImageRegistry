# =============================================================================
# SOVEREIGN META - SOURCE
# This is a metadata directory for source tracking, not a container image.
# =============================================================================


FROM scratch
LABEL org.opencontainers.image.title="source" \
      org.opencontainers.image.description="Meta directory for upstream source tracking. Not a runnable container." \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.image.category="meta" \
      sovereign.image.note="Source tracking directory, not a container image."

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
