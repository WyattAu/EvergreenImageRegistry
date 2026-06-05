
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg procps ; rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /opt/vernemq/data /opt/vernemq/log 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl procps
COPY --from=builder /app /app
COPY --from=builder /opt/vernemq /opt/vernemq
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /opt/vernemq -s /bin/false vernemq 2>/dev/null || true && \
    chown -R 65532:65532 /opt/vernemq /app 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/vernemq
EXPOSE 1883 4369 44053 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:1883"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "echo", "--", "vernemq: Place VerneMQ binary in /opt/vernemq/bin/"]
LABEL org.opencontainers.image.title="vernemq" \
      org.opencontainers.image.description="VerneMQ - High-performance MQTT broker" \
      org.opencontainers.image.vendor="VerneMQ" \
      org.opencontainers.image.source="https://github.com/vernemq/vernemq" \
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
