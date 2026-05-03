ARG VERSION=latest

FROM ghcr.io/cstate/cstate:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/statuspage /var/cache/statuspage 2>/dev/null || true


FROM scratch
COPY --from=upstream /cstate /cstate
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/statuspage /var/log/statuspage
COPY --from=builder /var/cache/statuspage /var/cache/statuspage

WORKDIR /app

EXPOSE 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="statuspage" org.opencontainers.image.version="5.7.0" org.opencontainers.image.vendor="cstate" org.opencontainers.image.source="https://github.com/cstate/cstate" org.opencontainers.image.description="Static status page generator" evergreen.image.tier="1" evergreen.image.category="monitoring" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.base="scratch" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="2000ms"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/cstate"]
