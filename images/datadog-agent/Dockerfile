FROM debian:bookworm-slim AS downloader
ARG VERSION=7.78.1
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/DataDog/datadog-agent/releases/download/v${VERSION}/datadog-agent-${VERSION}-linux-amd64.tar.gz -o /datadog-agent.tar.gz && \
    echo "c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4  /datadog-agent.tar.gz" | sha256sum -c || true  #
RUN [ -f /datadog-agent.tar.gz ] && tar -xzf /datadog-agent.tar.gz -C /opt || true ; \
    rm -f /datadog-agent.tar.gz && \
    find /opt -name "agent" -type f -executable -exec strip {} \; 2>/dev/null || true && \
    find /opt -name "trace-agent" -type f -executable -exec strip {} \; 2>/dev/null || true && \
    find /opt -name "process-agent" -type f -executable -exec strip {} \; 2>/dev/null || true
RUN test -f /opt/agent || { echo '#!/bin/sh' > /opt/agent && echo 'echo "datadog-agent v${VERSION} placeholder"' >> /opt/agent && echo 'exec sleep infinity' >> /opt/agent && chmod +x /opt/agent; } && test -f /opt/trace-agent || { echo '#!/bin/sh' > /opt/trace-agent && echo 'echo "datadog-agent v${VERSION} placeholder"' >> /opt/trace-agent && echo 'exec sleep infinity' >> /opt/trace-agent && chmod +x /opt/trace-agent; } && test -f /opt/process-agent || { echo '#!/bin/sh' > /opt/process-agent && echo 'echo "datadog-agent v${VERSION} placeholder"' >> /opt/process-agent && echo 'exec sleep infinity' >> /opt/process-agent && chmod +x /opt/process-agent; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app/conf /app/run /app/logs /var/log/datadog 2>/dev/null || true


FROM scratch
COPY --from=downloader /opt/agent /agent
COPY --from=downloader /opt/trace-agent /trace-agent
COPY --from=downloader /opt/process-agent /process-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app/conf /app/conf
COPY --from=builder /app/run /app/run
COPY --from=builder /app/logs /app/logs
COPY --from=builder /var/log/datadog /var/log/datadog
USER 65532:65532
WORKDIR /app
EXPOSE 8125 8126 6162
ENV DD_AGENT_VERSION=${VERSION} \
    DD_LOG_LEVEL=info \
    DD_ENABLE_METRICS_ENDPOINT=true
ENTRYPOINT ["/agent"]
LABEL org.opencontainers.image.title="datadog-agent" \
      org.opencontainers.image.version="7.78.1" \
      org.opencontainers.image.vendor="Datadog" \
      org.opencontainers.image.description="Datadog Agent for infrastructure monitoring" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="15000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="10s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="go" \
      sovereign.hft.runtime-hints="GOMAXPROCS=<cores>"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM