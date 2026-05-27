
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /opt/emqx || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg ; rm -rf /var/lib/apt/lists/* && \
    ARCH=$(case ${TARGETARCH} in amd64) echo "amd64" ;; arm64) echo "arm64" ;; *) echo "amd64" ;; esac) && \
    curl --retry 3 --retry-delay 5 -fsSL -o /emqx.tar.gz "https://www.emqx.com/en/downloads/broker/v5.8.0/emqx-5.8.0-debian12-${ARCH}.tar.gz" && \
    echo "95a8b8d0e51b2f9d0c7eab768aeb51e7e01ed290cd61a0a97092c2bb38815d58  /emqx.tar.gz" | sha256sum -c && \
    mkdir -p /opt/emqx ; \
    [ -f /emqx.tar.gz ] && tar -xzf /emqx.tar.gz -C /opt/emqx --strip-components=1 && rm -f /emqx.tar.gz && \
    mkdir -p /app /opt/emqx/data /opt/emqx/log 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates curl procps
COPY --from=builder /opt/emqx /opt/emqx
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /opt/emqx -s /bin/false emqx 2>/dev/null || true && \
    chown -R 65532:65532 /opt/emqx /app 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/emqx
EXPOSE 1883 8083 8084 8883 18083

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:1883/ || exit 1
ENTRYPOINT ["/opt/emqx/bin/emqx"]
CMD ["foreground"]
LABEL org.opencontainers.image.title="emqx" \
      org.opencontainers.image.description="EMQX - High-performance MQTT broker" \
      org.opencontainers.image.vendor="EMQ" \
      org.opencontainers.image.source="https://github.com/emqx/emqx" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.version="5.8.0"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
