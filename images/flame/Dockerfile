ARG VERSION=latest
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM pawelmalak/flame:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/flame /var/cache/flame 2>/dev/null || true


FROM scratch
RUN mkdir -p /etc/ssl/certs || true && touch /etc/ssl/certs/ca-certificates.crt || true
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN touch /flame || true
COPY --from=upstream /flame /flame
RUN mkdir -p /app || true
COPY --from=builder /app /app
RUN mkdir -p /var/log/flame || true
COPY --from=builder /var/log/flame /var/log/flame
RUN mkdir -p /var/cache/flame || true
COPY --from=builder /var/cache/flame /var/cache/flame

WORKDIR /app

EXPOSE 5005
EXPOSE 9101

LABEL org.opencontainers.image.title="flame" org.opencontainers.image.description="Flame - Self-hosted start page" org.opencontainers.image.vendor="pawelmalak" org.opencontainers.image.source="https://github.com/pawelmalak/flame" evergreen.image.tier="3" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="latest"
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
ENTRYPOINT ["/flame"]
