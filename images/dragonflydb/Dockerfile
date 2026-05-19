ARG VERSION=v1.38.1
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM ghcr.io/dragonflydb/dragonfly:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/dragonflydb /var/cache/dragonflydb 2>/dev/null || true


FROM scratch
RUN touch /dragonfly || true
COPY --from=upstream /usr/local/bin/dfly /dragonfly
RUN touch /etc/ssl/certs/ca-certificates.crt || true
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app || true
COPY --from=builder /app /app
RUN mkdir -p /var/log/dragonflydb || true
COPY --from=builder /var/log/dragonflydb /var/log/dragonflydb
RUN mkdir -p /var/cache/dragonflydb || true
COPY --from=builder /var/cache/dragonflydb /var/cache/dragonflydb

WORKDIR /app

EXPOSE 6379
EXPOSE 9101

LABEL org.opencontainers.image.title="dragonflydb" org.opencontainers.image.version="1.18.0" org.opencontainers.image.vendor="DragonflyDB" org.opencontainers.image.source="https://github.com/dragonflydb/dragonfly" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms" \
      org.opencontainers.image.description="dragonflydb container image" \
evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/dragonfly"]

CMD ["--bind", "0.0.0.0:6379"]
