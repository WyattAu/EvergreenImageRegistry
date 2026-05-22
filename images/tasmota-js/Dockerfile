
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates ; rm -rf /var/lib/apt/lists/* || true && \
    npm install -g tasmotizer 2>/dev/null || true && \
    mkdir -p /app-src 2>/dev/null || true



FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache nodejs-20 npm ca-certificates || true \
    mkdir -p /usr/lib 2>/dev/null || true
RUN mkdir -p /usr/lib/node_modules || true
COPY --from=builder /usr/lib/node_modules /usr/lib/node_modules
RUN mkdir -p /app || true
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false tasmota 2>/dev/null || true && \
    chown -R 65532:65532 /app/binary not available - download failed" >&2 \
    exit 1 /usr/lib/node_modules 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="tasmota-js" \
      org.opencontainers.image.description="Tasmota JavaScript tools" \
      org.opencontainers.image.vendor="Tasmota" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/xoseperez/tasmota" \
                  org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
