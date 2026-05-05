ARG VERSION=latest

FROM ghcr.io/kanidm/server:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/kanidm-server /var/cache/kanidm-server 2>/dev/null || true


FROM scratch
COPY --from=upstream /usr/local/bin/kanidmd /kanidmd
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kanidm-server /var/log/kanidm-server
COPY --from=builder /var/cache/kanidm-server /var/cache/kanidm-server

WORKDIR /app

EXPOSE 8443
EXPOSE 9101

LABEL org.opencontainers.image.title="kanidm-server" org.opencontainers.image.version="1.9.2" org.opencontainers.image.vendor="Kanidm" org.opencontainers.image.source="https://github.com/kanidm/kanidm" evergreen.image.tier="2" evergreen.image.category="identity" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms" \
      org.opencontainers.image.description="kanidm-server container image" \
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
ENTRYPOINT ["/kanidmd"]
