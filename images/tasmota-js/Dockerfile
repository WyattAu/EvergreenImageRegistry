FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g tasmotizer 2>/dev/null || true
RUN mkdir -p /app

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache nodejs npm ca-certificates
COPY --from=builder /usr/lib/node_modules /usr/lib/node_modules 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin tasmota 2>/dev/null || true && \
    chown -R 65532:65532 /app /usr/lib/node_modules 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="tasmota-js" \
      org.opencontainers.image.description="Tasmota JavaScript tools" \
      org.opencontainers.image.vendor="Tasmota" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM