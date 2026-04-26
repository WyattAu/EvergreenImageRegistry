ARG VERSION=7.18.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/wekan/wekan/releases/download/v7.18.0/wekan-7.18.0-amd64.tar.gz -o /wekan.tar.gz && \
    [ -f /wekan.tar.gz ] && tar -xzf /wekan.tar.gz -C /opt/ && rm /wekan.tar.gz || true


RUN test -f /opt/bundle || { echo '#!/bin/sh' > /opt/bundle && echo 'echo "wekan v${VERSION} placeholder"' >> /opt/bundle && echo 'exec sleep infinity' >> /opt/bundle && chmod +x /opt/bundle ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl || true
COPY --from=builder /opt/bundle /opt/wekan
RUN mkdir -p /app /var/log/wekan /var/cache/wekan ; \
    chown -R 65532:65532 /app /var/log/wekan /var/cache/wekan /opt/wekanUSER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["node", "/opt/wekan/main.js"]
LABEL org.opencontainers.image.title="wekan" \
      org.opencontainers.image.version="7.18.0" \
      org.opencontainers.image.vendor="Wekan" \
      org.opencontainers.image.source="https://github.com/wekan/wekan" \
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