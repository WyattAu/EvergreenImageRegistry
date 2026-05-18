ARG VERSION=v8.5.6
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM pingcap/tidb:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/tidb /var/cache/tidb 2>/dev/null || true


FROM scratch
COPY --from=upstream /tidb-server /usr/local/bin/tidb-server
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tidb /var/log/tidb
COPY --from=builder /var/cache/tidb /var/cache/tidb

EXPOSE 4000 10080
EXPOSE 9101

LABEL org.opencontainers.image.title="tidb" org.opencontainers.image.description="Evergreen hardened TiDB - distributed NewSQL database" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.vendor="PingCAP" evergreen.image.status="functional" evergreen.image.tier="1" evergreen.image.category="database" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" \
      org.opencontainers.image.source="https://github.com/pingcap/tidb"
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
ENTRYPOINT ["/usr/local/bin/tidb-server"]
