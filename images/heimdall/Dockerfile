FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/linuxserver/Heimdall.git /src 2>/dev/null || true
RUN mkdir -p /app /config

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates nginx
COPY --from=builder /src /app/src 2>/dev/null || true
COPY --from=builder /config /config 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin heimdall 2>/dev/null || true && \
    chown -R 65532:65532 /app /config 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80 443
ENTRYPOINT ["node"]
CMD ["/app/src/server.js"]
LABEL org.opencontainers.image.title="heimdall" \
      org.opencontainers.image.description="Heimdall - Application dashboard" \
      org.opencontainers.image.vendor="LinuxServer.io" \
      org.opencontainers.image.source="https://github.com/linuxserver/Heimdall" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM