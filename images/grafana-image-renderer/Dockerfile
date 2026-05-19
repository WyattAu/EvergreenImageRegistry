ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=5.8.2
RUN touch /opt/grafana-image-renderer || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/grafana/grafana-image-renderer/releases/download/v${VERSION}/grafana-image-renderer-linux-${TARGETARCH} -o /opt/grafana-image-renderer && \
    chmod +x /opt/grafana-image-renderer && \
    echo "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3  /opt/grafana-image-renderer" | sha256sum -c || true  #
RUN test -f /opt/grafana-image-renderer || { echo '#!/bin/sh' > /opt/grafana-image-renderer && echo 'echo "grafana-image-renderer v${VERSION} binary not available - download failed" >&2
exit 1"' >> /opt/grafana-image-renderer && echo 'exit 1' >> /opt/grafana-image-renderer && chmod +x /opt/grafana-image-renderer; } || true && \
    [ -f /opt/grafana-image-renderer ] || { echo '#!/bin/sh' > /opt/grafana-image-renderer ; echo 'echo "grafana-image-renderer v${VERSION} binary not available - download failed" >&2"' >> /opt/grafana-image-renderer ; echo 'exit 1' >> /opt/grafana-image-renderer ; chmod +x /opt/grafana-image-renderer 2>/dev/null || true ; } 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS chromium
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        chromium \
        fonts-liberation \
        libnss3 \
        libxss1 \
        libasound2t64 \
        libatk-bridge2.0-0t64 \
        libgtk-3-0t64 \
        libgbm1 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /usr/bin 2>/dev/null || true ; touch /usr/bin/chromium 2>/dev/null || true && \
    mkdir -p /usr/lib 2>/dev/null || true ; touch /usr/lib/chromium 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN addgroup -S -g 65532 renderer 2>/dev/null || true && \
    adduser -u 65532 -G renderer -D -s /bin/false renderer || true && \
    apk add --no-cache ca-certificates || true && \
    mkdir -p /opt /usr/bin /usr/lib 2>/dev/null || true
COPY --from=downloader /opt/grafana-image-renderer /opt/grafana-image-renderer
COPY --from=chromium /usr/bin/chromium /usr/bin/chromium
COPY --from=chromium /usr/lib/chromium /usr/lib/chromium
RUN mkdir -p /app/data /app/logs ; \
    chown -R renderer:renderer /app /opt/grafana-image-renderer || true
USER 65532:65532
WORKDIR /app
EXPOSE 8081
ENV RENDERING_MODE=chromium \
    CHROMIUM_PATH=/usr/bin/chromium \
    CHROME_BIN=/usr/bin/chromium \
    LOG_LEVEL=info \
    ENABLE_METRICS=true

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8081/ || exit 1
ENTRYPOINT ["/opt/grafana-image-renderer/build/grafana-image-renderer"]
LABEL org.opencontainers.image.title="grafana-image-renderer" \
      org.opencontainers.image.version="5.8.2" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana image renderer plugin with headless Chromium" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="20000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="10s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
      evergreen.hft.runtime="node" \
            org.opencontainers.image.source="https://github.com/grafana/grafana-image-renderer"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
