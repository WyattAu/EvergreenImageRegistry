# =============================================================================
# SOVEREIGN META - GRUB
# This is a metadata directory for bootloader config, not a container image.
# =============================================================================


FROM scratch
USER 65532:65532
LABEL org.opencontainers.image.title="grub" \
      org.opencontainers.image.description="Meta directory for GRUB bootloader configuration. Not a runnable container." \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.image.category="meta" \
      sovereign.image.note="Bootloader config directory, not a container image."

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
