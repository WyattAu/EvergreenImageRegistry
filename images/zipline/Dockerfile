FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app/data /var/log/zipline /var/cache/zipline

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache nodejs npm git ca-certificates python3 make
WORKDIR /src
RUN git clone --depth 1 https://github.com/diced/zipline.git /src && \
    cd /src && npm ci && npm run build
RUN mkdir -p /app/data
COPY --from=downloader /app/data /app/data
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin zipline 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app/src
EXPOSE 8080
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="zipline" \
      org.opencontainers.image.description="Zipline - File sharing platform" \
      org.opencontainers.image.vendor="diced" \
      org.opencontainers.image.source="https://github.com/diced/zipline" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM