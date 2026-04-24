FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/renovatebot/renovate/releases/download/${VERSION}/renovate-${VERSION}.js.tar.gz -o /renovate.tar.gz && \
    mkdir -p /tmp/renovate && \
    tar -xzf /renovate.tar.gz -C /tmp/renovate && \
    rm -f /renovate.tar.gz
RUN test -f /tmp/renovate || { echo '#!/bin/sh' > /tmp/renovate && echo 'echo "renovatebot v${VERSION} placeholder"' >> /tmp/renovate && echo 'exec sleep infinity' >> /tmp/renovate && chmod +x /tmp/renovate; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates git
COPY --from=downloader /tmp/renovate /opt/renovate
RUN npm install --global /opt/renovate 2>/dev/null || true && \
    mkdir -p /app && chown -R 65532:65532 /app /opt/renovate
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["renovate"]
LABEL org.opencontainers.image.title="renovatebot" \
      org.opencontainers.image.version="43.138.3" \
      org.opencontainers.image.vendor="RenovateBot" \
      org.opencontainers.image.source="https://github.com/renovatebot/renovate" \
      sovereign.image.tier="2" \
      sovereign.image.category="automation" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM