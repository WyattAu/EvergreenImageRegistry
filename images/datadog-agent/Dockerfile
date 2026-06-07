ARG VERSION=7.67.1
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM datadog/agent:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app/conf /app/run /app/logs /var/log/datadog 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=upstream /opt/datadog/bin/agent /agent
COPY --from=upstream /opt/datadog/bin/trace-agent /trace-agent
COPY --from=upstream /opt/datadog/bin/process-agent /process-agent
COPY --from=builder /app/conf /app/conf
COPY --from=builder /app/run /app/run
COPY --from=builder /app/logs /app/logs
COPY --from=builder /var/log/datadog /var/log/datadog

ENV DD_AGENT_VERSION=${VERSION} DD_LOG_LEVEL=info DD_ENABLE_METRICS_ENDPOINT=true

WORKDIR /app

EXPOSE 8125 8126 6162
EXPOSE 9101

LABEL org.opencontainers.image.title="datadog-agent" org.opencontainers.image.version="7.78.1" org.opencontainers.image.vendor="Datadog" org.opencontainers.image.description="Datadog Agent for infrastructure monitoring" evergreen.image.tier="1" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="5s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="15000ms" evergreen.hft.cpu-pins="4-5" evergreen.hft.cpu-pins-mode="shared" evergreen.hft.deploy-strategy="standard-rolling" evergreen.hft.pre-stop-hook="true" evergreen.hft.pre-stop-delay="10s" evergreen.hft.connection-drain="true" evergreen.hft.sched-policy="SCHED_OTHER" evergreen.hft.runtime="go" evergreen.hft.runtime-hints="GOMAXPROCS=<cores>" \
      org.opencontainers.image.source="https://github.com/DataDog/datadog-agent"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8125"]

ENTRYPOINT ["/shim", "run"]
