ARG VERSION=latest

FROM pingcap/tidb:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/tidb-lightning /var/cache/tidb-lightning 2>/dev/null || true


FROM scratch
COPY --from=upstream /tidb-lightning /usr/local/bin/tidb-lightning
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tidb-lightning /var/log/tidb-lightning
COPY --from=builder /var/cache/tidb-lightning /var/cache/tidb-lightning

EXPOSE 8289
EXPOSE 9101

LABEL org.opencontainers.image.title="tidb-lightning" org.opencontainers.image.description="Evergreen hardened TiDB Lightning - high-speed TiDB data import tool" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.vendor="PingCAP" evergreen.image.status="functional" evergreen.image.tier="1" evergreen.image.category="database" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/tidb-lightning"]
