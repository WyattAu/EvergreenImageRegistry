# =============================================================================
# EVERGREEN META - GRUB
# This is a metadata directory for bootloader config, not a container image.
# =============================================================================


FROM scratch
USER 65532:65532
LABEL org.opencontainers.image.title="grub" \
      org.opencontainers.image.description="Meta directory for GRUB bootloader configuration. Not a runnable container." \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.image.category="meta" \
      evergreen.image.note="Bootloader config directory, not a container image." \
            org.opencontainers.image.source="https://github.com/coreos/grub" \
                  org.opencontainers.image.version="unknown"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
