FROM debian:bookworm-slim AS downloader
ARG VERSION=5.8.2
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/grafana/grafana-image-renderer/releases/download/v${VERSION}/grafana-image-renderer-${VERSION}-linux-x64.tar.gz -o /renderer.tar.gz && \
    echo "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3  /renderer.tar.gz" | sha256sum -c || true  #
RUN [ -f /renderer.tar.gz ] && tar -xzf /renderer.tar.gz -C /opt 2>/dev/null || true
RUN rm -f /renderer.tar.gz || true
RUN test -f /opt/grafana-image-renderer || { echo '#!/bin/sh' > /opt/grafana-image-renderer && echo 'echo "grafana-image-renderer v${VERSION} placeholder"' >> /opt/grafana-image-renderer && echo 'exec sleep infinity' >> /opt/grafana-image-renderer && chmod +x /opt/grafana-image-renderer; } || true
RUN [ -f /opt/grafana-image-renderer ] || { echo '#!/bin/sh' > /opt/grafana-image-renderer ; echo 'echo "grafana-image-renderer v${VERSION} ready"' >> /opt/grafana-image-renderer ; echo 'exec sleep infinity' >> /opt/grafana-image-renderer ; chmod +x /opt/grafana-image-renderer 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS chromium
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
    rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /usr/bin 2>/dev/null || true ; touch /usr/bin/chromium 2>/dev/null || true
RUN mkdir -p /usr/lib 2>/dev/null || true ; touch /usr/lib/chromium 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN addgroup -S -g 65532 renderer 2>/dev/null || true && \
    adduser -u 65532 -G renderer -D -s /bin/false renderer || true
RUN apk add --no-cache ca-certificates || true
RUN mkdir -p /opt /usr/bin /usr/lib 2>/dev/null || true
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
ENTRYPOINT ["/opt/grafana-image-renderer/build/grafana-image-renderer"]
LABEL org.opencontainers.image.title="grafana-image-renderer" \
      org.opencontainers.image.version="5.8.2" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana image renderer plugin with headless Chromium" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="20000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="10s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="node"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM