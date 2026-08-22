ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base:0.30.1
COPY --from=ghcr.io/wyattau/evergreenshim/health-shim:v2.0.0 /shim /usr/local/bin/shim
ARG VERSION=0.30.1
RUN apk add --no-cache ruby ca-certificates git openssh && \
    gem install oxidized && \
    mkdir -p /home/oxidized/.config/oxidized
USER 65532:65532
WORKDIR /home/oxidized
EXPOSE 8888 9101
LABEL evergreen.entrypoint.pattern="direct"
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8888"]
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "oxidized"]
LABEL org.opencontainers.image.title="oxidized" \
      org.opencontainers.image.source="https://github.com/ytti/oxidized" \
      org.opencontainers.image.version="0.30.1" \
      org.opencontainers.image.description="Oxidized - network configuration management" \
      evergreen.base.image="wolfi"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="standard"
