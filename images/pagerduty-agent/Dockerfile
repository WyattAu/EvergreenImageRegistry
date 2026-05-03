ARG VERSION=latest

FROM pagerduty/pdagent:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
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

LABEL org.opencontainers.image.title="pagerduty-agent" org.opencontainers.image.version="1.7.4" org.opencontainers.image.vendor="PagerDuty" org.opencontainers.image.source="https://github.com/PagerDuty/pdagent" evergreen.image.tier="2" evergreen.image.category="monitoring" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/pdagent"]
