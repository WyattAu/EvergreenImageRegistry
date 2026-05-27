
ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates && \
    pip install --break-system-packages --no-cache-dir zigpy==0.60.0 2>/dev/null && \
    addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false zoe 2>/dev/null || true && \
    mkdir -p /app && chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
CMD ["/bin/sh"]
LABEL org.opencontainers.image.description="zoe container image" \
      org.opencontainers.image.title="Zoe" \
      org.opencontainers.image.source="https://github.com/eclipse-zenoh/zenoh-pico" \
            org.opencontainers.image.version="unknown"
