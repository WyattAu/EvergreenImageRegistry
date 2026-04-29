ARG VERSION=9.01
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg unzip && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/wekan/wekan/releases/download/v${VERSION}/wekan-${VERSION}-amd64.zip -o /wekan.zip || true
RUN if [ -f /wekan.zip ]; then unzip -q /wekan.zip -d /opt/ && rm /wekan.zip; fi

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 
COPY --from=builder /opt/bundle /opt/wekan
RUN mkdir -p /app /var/log/wekan /var/cache/wekan /opt/wekan 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/wekan /var/cache/wekan /opt/wekan
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["node", "/opt/wekan/main.js"]
LABEL org.opencontainers.image.title="wekan" \
      org.opencontainers.image.version="9.01" \
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