ARG VERSION=0.65.22
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app /var/log/airbyte-worker /var/cache/airbyte-worker /var/lib/airbyte 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates 
COPY --from=builder /app /app
COPY --from=builder /var/log/airbyte-worker /var/log/airbyte-worker
COPY --from=builder /var/cache/airbyte-worker /var/cache/airbyte-worker
COPY --from=builder /var/lib/airbyte /var/lib/airbyte
RUN adduser -u 65532 -D airbyte 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["java", "-jar", "/app/worker.jar"]
LABEL org.opencontainers.image.title="airbyte-worker" \
      org.opencontainers.image.version="0.65.22" \
      org.opencontainers.image.vendor="Airbyte" \
      org.opencontainers.image.description="Evergreen hardened airbyte-worker - Airbyte worker process" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
