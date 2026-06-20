ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make gcc libavahi-compat-libdnssd-dev ; rm -rf /var/lib/apt/lists/* && \
    npm install -g --unsafe-perm homebridge hap-nodejs 2>/dev/null && \
    mkdir -p /usr/lib/node_modules/homebridge/bin /usr/lib/node_modules/hap-nodejs /app /homebridge 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache nodejs-20 npm ca-certificates && \
    mkdir -p /usr/lib/node_modules /app /homebridge 2>/dev/null || true
COPY --from=builder /usr/lib/node_modules/homebridge /usr/lib/node_modules/homebridge
COPY --from=builder /usr/lib/node_modules/hap-nodejs /usr/lib/node_modules/hap-nodejs
COPY --from=builder /app /app
COPY --from=builder /homebridge /homebridge
RUN ln -sf /usr/lib/node_modules/homebridge/bin/homebridge /usr/local/bin/homebridge 2>/dev/null || true && \
    addgroup -S -g 10000 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -h /homebridge -s /bin/false homebridge 2>/dev/null || true && \
    chown -R 65532:65532 /homebridge /app /usr/lib/node_modules 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /homebridge
EXPOSE 51826

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:51826"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "homebridge"]
LABEL org.opencontainers.image.title="homebridge" \
      org.opencontainers.image.description="Homebridge - Bring Siri to your smart home" \
      org.opencontainers.image.vendor="nfarina" \
      org.opencontainers.image.source="https://github.com/nfarina/homebridge" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
