FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g iobroker
RUN mkdir -p /app /opt/iobroker

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache nodejs npm ca-certificates
COPY --from=builder /opt/iobroker /opt/iobroker
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /opt/iobroker -s /sbin/nologin iobroker 2>/dev/null || true && \
    chown -R 65532:65532 /opt/iobroker /app 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/iobroker
EXPOSE 8081 3000
ENTRYPOINT ["iobroker"]
CMD ["start"]
LABEL org.opencontainers.image.title="iobroker" \
      org.opencontainers.image.description="ioBroker - IoT automation platform" \
      org.opencontainers.image.vendor="ioBroker" \
      org.opencontainers.image.source="https://github.com/ioBroker/ioBroker" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM