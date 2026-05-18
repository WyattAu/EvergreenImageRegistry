
ARG APP_UID=65532
ARG APP_GID=65532

FROM scratch
USER 65532:65532
LABEL org.opencontainers.image.title="amd64" \
      org.opencontainers.image.description="Evergreen hardened amd64 - AMD64 architecture base image" \
      evergreen.image.tier="3" \
      evergreen.image.note="Placeholder base image for AMD64 architecture. Extend with application binaries."

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
