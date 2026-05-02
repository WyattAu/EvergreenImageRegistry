ARG VERSION=latest

FROM pingcap/tidb:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/tidb /var/cache/tidb 2>/dev/null || true


FROM scratch
COPY --from=upstream /tidb-server /usr/local/bin/tidb-server
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tidb /var/log/tidb
COPY --from=builder /var/cache/tidb /var/cache/tidb

EXPOSE 4000 10080
EXPOSE 9101

LABEL org.opencontainers.image.title="tidb" org.opencontainers.image.description="Sovereign hardened TiDB - distributed NewSQL database" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.vendor="PingCAP" sovereign.image.status="functional" sovereign.image.tier="1" sovereign.image.category="database" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/usr/local/bin/tidb-server"]
