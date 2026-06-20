ARG TARGETARCH

ARG VERSION=0.3.0b2
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN apk add --no-cache ca-certificates python3 py3-pip && \
    pip3 install --break-system-packages --no-cache-dir maxbot==${VERSION} && \
    addgroup -g 65532 app 2>/dev/null || true && \
    adduser -D -u 65532 -G app app 2>/dev/null || true && \
    mkdir -p /app /var/log/maxbot /var/cache/maxbot 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/maxbot /var/cache/maxbot 2>/dev/null || true
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "maxbot"]
LABEL org.opencontainers.image.title="maxbot" \
      org.opencontainers.image.description="Maxbot - open source framework for creating conversational apps" \
      org.opencontainers.image.version="0.3.0b2" \
      org.opencontainers.image.vendor="Maxbot team" \
      org.opencontainers.image.source="https://github.com/maxbot-ai/maxbot" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM
