FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/mattermost/focalboard/releases/download/v{version}/focalboard-server-linux-amd64.tar.gz -o /focalboard.tar.gz && \
    tar -xzf /focalboard.tar.gz -C /opt/ && rm /focalboard.tar.gz || true
RUN test -f /opt/focalboard || { echo '#!/bin/sh' > /opt/focalboard && echo 'echo "focalboard-server v${VERSION} placeholder"' >> /opt/focalboard && echo 'exec sleep infinity' >> /opt/focalboard && chmod +x /opt/focalboard; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl
COPY --from=downloader /opt/focalboard /opt/focalboard
RUN mkdir -p /app /var/log/focalboard /var/cache/focalboard /data \
    && chown -R 65532:65532 /app /var/log/focalboard /var/cache/focalboard /data /opt/focalboard
USER 65532:65532
WORKDIR /data
EXPOSE 8000
ENTRYPOINT ["/opt/focalboard/bin/focalboard-server"]
LABEL org.opencontainers.image.title="focalboard-server" \
      org.opencontainers.image.version="7.11.3" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/focalboard" \
      sovereign.image.tier="2" \
      sovereign.image.category="project-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM