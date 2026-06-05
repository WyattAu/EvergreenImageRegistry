
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /opt/emqx || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates ; rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /opt/emqx/data /opt/emqx/log 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl procps
COPY --from=builder /app /app
COPY --from=builder /opt/emqx /opt/emqx
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /opt/emqx -s /bin/false emqx 2>/dev/null || true && \
    chown -R 65532:65532 /opt/emqx /app 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/emqx
EXPOSE 1883 8083 8084 8883 18083

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:1883"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "echo", "--", "emqx-ee: Enterprise edition requires license. Place emqx binary in /opt/emqx/bin/"]
LABEL org.opencontainers.image.title="emqx-ee" \
      org.opencontainers.image.description="EMQX Enterprise - requires license" \
      org.opencontainers.image.vendor="EMQ" \
      org.opencontainers.image.source="https://github.com/emqx/emqx" \
      evergreen.image.tier="3" \
      evergreen.image.status="license-required" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
