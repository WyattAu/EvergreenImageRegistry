ARG VERSION=latest

FROM pagerduty/pdagent:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/pagerduty-agent /var/cache/pagerduty-agent 2>/dev/null || true


FROM scratch
COPY --from=upstream /pdagent /pdagent
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pagerduty-agent /var/log/pagerduty-agent
COPY --from=builder /var/cache/pagerduty-agent /var/cache/pagerduty-agent

WORKDIR /app

EXPOSE 4550
EXPOSE 9101

LABEL org.opencontainers.image.title="pagerduty-agent" org.opencontainers.image.version="1.7.4" org.opencontainers.image.vendor="PagerDuty" org.opencontainers.image.source="https://github.com/PagerDuty/pdagent" sovereign.image.tier="2" sovereign.image.category="monitoring" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/pdagent"]
