
FROM scratch
USER 65532:65532
LABEL org.opencontainers.image.title="aarch64-unknown-linux-musl" \
      org.opencontainers.image.description="Evergreen hardened aarch64-unknown-linux-musl - ARM64 musl static base" \
      evergreen.image.tier="3" \
      evergreen.image.note="Placeholder base image for ARM64 musl static binaries. Extend with application binaries."

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
