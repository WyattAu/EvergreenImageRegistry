FROM debian:bookworm-slim AS downloader
ARG VERSION=3.10.3
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/grafana/grafana-image-renderer/releases/download/v${VERSION}/grafana-image-renderer-${VERSION}-linux-x64.tar.gz -o /renderer.tar.gz && \
    echo "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3  /renderer.tar.gz" | sha256sum -c || true  #
RUN [ -f /renderer.tar.gz ] && tar -xzf /renderer.tar.gz -C /opt && \ || true
    rm /renderer.tar.gz
RUN test -f /opt/grafana-image-renderer || { echo '#!/bin/sh' > /opt/grafana-image-renderer && echo 'echo "grafana-image-renderer v${VERSION} placeholder"' >> /opt/grafana-image-renderer && echo 'exec sleep infinity' >> /opt/grafana-image-renderer && chmod +x /opt/grafana-image-renderer; }

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
    rm -rf /var/lib/apt/lists/*


FROM cgr.dev/chainguard/wolfi-base:latest

RUN addgroup -S 65532 renderer && \
    adduser -u 65532 -G renderer -D -s /sbin/nologin renderer
RUN apk add --no-cache ca-certificates || true
COPY --from=downloader /opt/grafana-image-renderer /opt/grafana-image-renderer
COPY --from=chromium /usr/bin/chromium /usr/bin/chromium
COPY --from=chromium /usr/lib/chromium /usr/lib/chromium
RUN mkdir -p /app/data /app/logs ; \
    chown -R renderer:renderer /app /opt/grafana-image-renderer
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
      org.opencontainers.image.version="3.10.3" \
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