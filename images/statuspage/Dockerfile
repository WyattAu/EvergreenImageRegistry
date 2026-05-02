ARG VERSION=latest

FROM ghcr.io/cstate/cstate:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
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

LABEL org.opencontainers.image.title="statuspage" org.opencontainers.image.version="5.7.0" org.opencontainers.image.vendor="cstate" org.opencontainers.image.source="https://github.com/cstate/cstate" org.opencontainers.image.description="Static status page generator" sovereign.image.tier="1" sovereign.image.category="monitoring" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.base="scratch" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="2000ms"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/cstate"]
