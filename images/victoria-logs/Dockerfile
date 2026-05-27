
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=v1.50.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/VictoriaMetrics/VictoriaLogs/releases/download/v1.50.0/victoria-logs-linux-amd64-v1.50.0.tar.gz -o /victoria-logs.tar.gz && \
    [ -f /victoria-logs.tar.gz ] && tar -xzf /victoria-logs.tar.gz -C / && rm -f /victoria-logs.tar.gz && chmod +x /victoria-logs-prod 2>/dev/null ; \binary not available - download failed" >&2"' >> /victoria-logs-prod && echo 'exit 1' >> /victoria-logs-prod && chmod +x /victoria-logs-prod; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/victoria-logs /var/cache/victoria-logs 2>/dev/null || true


FROM scratch
COPY --from=downloader /victoria-logs-prod /victoria-logs-prod
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/victoria-logs /var/log/victoria-logs
COPY --from=builder /var/cache/victoria-logs /var/cache/victoria-logs
USER 65532:65532
WORKDIR /app
EXPOSE 9428

HEALTHCHECK NONE
ENTRYPOINT ["/victoria-logs-prod"]
LABEL org.opencontainers.image.title="victoria-logs" \
      org.opencontainers.image.description="VictoriaLogs - logs storage by VictoriaMetrics" \
      org.opencontainers.image.version="v1.50.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/VictoriaMetrics/VictoriaLogs"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
