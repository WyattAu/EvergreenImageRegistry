ARG VERSION=2.0.10
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/node /var/cache/node


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs ca-certificates curl
COPY --from=builder /app /app
RUN mkdir -p /app /var/log/node /var/cache/node \
    && chown -R 65532:65532 /app /var/log/node /var/cache/node
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="rclone-browser" \
      org.opencontainers.image.version="2.0.10" \
      org.opencontainers.image.vendor="Rclone Browser" \
      org.opencontainers.image.source="https://github.com/rclone/rclone-webui-react" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
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