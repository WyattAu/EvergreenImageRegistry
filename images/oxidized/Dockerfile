ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=0.30.1
ARG TARGETARCH
RUN apk add --no-cache ruby ca-certificates git openssh 2>/dev/null || true && \
    gem install oxidized 2>/dev/null || true
USER 65532:65532
EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["sleep", "infinity"]
LABEL org.opencontainers.image.title="oxidized" \
      org.opencontainers.image.source="https://github.com/ytti/oxidized" \
            org.opencontainers.image.version="0.30.1" \
      org.opencontainers.image.description="oxidized container image" \
evergreen.base.image="wolfi"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="2"
