ARG VERSION=latest

FROM ghcr.io/kanidm/kanidm:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kanidm /var/cache/kanidm 2>/dev/null || true


FROM scratch
COPY --from=upstream /usr/local/bin/kanidm /kanidm
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kanidm /var/log/kanidm
COPY --from=builder /var/cache/kanidm /var/cache/kanidm

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="kanidm" org.opencontainers.image.version="1.9.2" org.opencontainers.image.vendor="Kanidm" org.opencontainers.image.source="https://github.com/kanidm/kanidm" sovereign.image.tier="2" sovereign.image.category="identity" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/kanidm"]
