# =============================================================================
# SOVEREIGN META - CATEGORY
# This is a metadata/classification directory, not a container image.
# Used for organizing image categories in the registry.
# =============================================================================


FROM scratch
USER 65532:65532
LABEL org.opencontainers.image.title="category" \
      org.opencontainers.image.description="Meta directory for image classification. Not a runnable container." \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.image.category="meta" \
      sovereign.image.note="Classification directory, not a container image."

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
