ARG VERSION=latest

FROM docker.dragonflydb.io/dragonfly:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/dragonflydb /var/cache/dragonflydb 2>/dev/null || true


FROM scratch
COPY --from=upstream /usr/local/bin/dfly /dragonfly
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/dragonflydb /var/log/dragonflydb
COPY --from=builder /var/cache/dragonflydb /var/cache/dragonflydb

WORKDIR /app

EXPOSE 6379
EXPOSE 9101

LABEL org.opencontainers.image.title="dragonflydb" org.opencontainers.image.version="1.18.0" org.opencontainers.image.vendor="DragonflyDB" org.opencontainers.image.source="https://github.com/dragonflydb/dragonfly" sovereign.image.tier="1" sovereign.image.category="database" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/dragonfly"]

CMD ["--bind", "0.0.0.0:6379"]
