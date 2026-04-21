# =============================================================================
# SOVEREIGN HARDENED DATADOG-AGENT
# Generated from template - Version: 7.50.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=7.50.0
ARG BUILD_DATE

FROM debian:bookworm-20240101-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/DataDog/datadog-agent/releases/download/v${VERSION}/datadog-agent-${VERSION}-linux-amd64.tar.gz" -o /datadog-agent.tar.gz && \
    echo "c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4  /datadog-agent.tar.gz" | sha256sum -c -
RUN tar -xzf /datadog-agent.tar.gz -C /opt && \
    rm /datadog-agent.tar.gz && \
    find /opt -name "agent" -type f -executable -exec strip {} \; 2>/dev/null || true && \
    find /opt -name "trace-agent" -type f -executable -exec strip {} \; 2>/dev/null || true && \
    find /opt -name "process-agent" -type f -executable -exec strip {} \; 2>/dev/null || true

FROM debian:bookworm-20240101-slim AS builder
RUN mkdir -p /app/conf /app/run /app/logs /var/log/datadog

FROM scratch
COPY --from=downloader /opt/agent /agent
COPY --from=downloader /opt/trace-agent /trace-agent
COPY --from=downloader /opt/process-agent /process-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app/conf /app/conf
COPY --from=builder /app/run /app/run
COPY --from=builder /app/logs /app/logs
COPY --from=builder /var/log/datadog /var/log/datadog
USER 65534:65534
WORKDIR /app
EXPOSE 8125 8126 6162
ENV DD_AGENT_VERSION=${VERSION} \
    DD_LOG_LEVEL=info \
    DD_ENABLE_METRICS_ENDPOINT=true
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/agent", "version"]
ENTRYPOINT ["/agent"]
LABEL org.opencontainers.image.title="datadog-agent" \
      org.opencontainers.image.version="7.50.0" \
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
