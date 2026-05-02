ARG VERSION=7

FROM gcr.io/datadoghq/agent:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app/conf /app/run /app/logs /var/log/datadog 2>/dev/null || true


FROM scratch
COPY --from=upstream /opt/datadog/bin/agent /agent
COPY --from=upstream /opt/datadog/bin/trace-agent /trace-agent
COPY --from=upstream /opt/datadog/bin/process-agent /process-agent
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app/conf /app/conf
COPY --from=builder /app/run /app/run
COPY --from=builder /app/logs /app/logs
COPY --from=builder /var/log/datadog /var/log/datadog

ENV DD_AGENT_VERSION=${VERSION} DD_LOG_LEVEL=info DD_ENABLE_METRICS_ENDPOINT=true

WORKDIR /app

EXPOSE 8125 8126 6162
EXPOSE 9101

LABEL org.opencontainers.image.title="datadog-agent" org.opencontainers.image.version="7.78.1" org.opencontainers.image.vendor="Datadog" org.opencontainers.image.description="Datadog Agent for infrastructure monitoring" sovereign.image.tier="1" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="5s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="15000ms" sovereign.hft.cpu-pins="4-5" sovereign.hft.cpu-pins-mode="shared" sovereign.hft.deploy-strategy="standard-rolling" sovereign.hft.pre-stop-hook="true" sovereign.hft.pre-stop-delay="10s" sovereign.hft.connection-drain="true" sovereign.hft.sched-policy="SCHED_OTHER" sovereign.hft.runtime="go" sovereign.hft.runtime-hints="GOMAXPROCS=<cores>"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/agent"]
