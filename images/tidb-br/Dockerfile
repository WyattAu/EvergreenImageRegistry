ARG VERSION=latest

FROM pingcap/tidb:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/tidb-br /var/cache/tidb-br 2>/dev/null || true


FROM scratch
COPY --from=upstream /br /usr/local/bin/br
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tidb-br /var/log/tidb-br
COPY --from=builder /var/cache/tidb-br /var/cache/tidb-br

EXPOSE 8289
EXPOSE 9101

LABEL org.opencontainers.image.title="tidb-br" org.opencontainers.image.description="Sovereign hardened TiDB BR - backup and restore tool for TiDB" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.vendor="PingCAP" sovereign.image.status="functional" sovereign.image.tier="1" sovereign.image.category="database" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/usr/local/bin/br"]
