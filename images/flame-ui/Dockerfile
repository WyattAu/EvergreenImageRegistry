ARG VERSION=v2.4.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM pawelmalak/flame:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/flame-ui /var/cache/flame-ui 2>/dev/null || true


FROM scratch
COPY --from=upstream /app/flame /usr/local/bin/flame
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/flame-ui /var/log/flame-ui
COPY --from=builder /var/cache/flame-ui /var/cache/flame-ui

WORKDIR /app

EXPOSE 5005
EXPOSE 9101

LABEL org.opencontainers.image.title="flame-ui" org.opencontainers.image.description="Flame - UI variant" org.opencontainers.image.vendor="pawelmalak" org.opencontainers.image.source="https://github.com/pawelmalak/flame" evergreen.image.tier="3" evergreen.constraint.nonroot="true" evergreen.base.image="scratch" \
      org.opencontainers.image.version="latest"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["flame"]

CMD ["--ui-only"]
