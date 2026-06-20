ARG VERSION=0.65.22
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/lib/airbyte || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /var/log/airbyte-worker /var/cache/airbyte-worker /var/lib/airbyte 2>/dev/null || true
ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim

RUN apk add --no-cache ca-certificates
COPY --from=builder /app /app
COPY --from=builder /var/log/airbyte-worker /var/log/airbyte-worker
COPY --from=builder /var/cache/airbyte-worker /var/cache/airbyte-worker
COPY --from=builder /var/lib/airbyte /var/lib/airbyte
RUN adduser -u 65532 -D airbyte 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "java -jar /app/worker.jar"]
LABEL org.opencontainers.image.title="airbyte-worker" \
      org.opencontainers.image.version="0.65.22" \
      org.opencontainers.image.vendor="Airbyte" \
      org.opencontainers.image.description="Evergreen hardened airbyte-worker - Airbyte worker process" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
            org.opencontainers.image.source="https://github.com/airbytehq/airbyte"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
