ARG VERSION=latest

FROM ghcr.io/clonezilla/keynuker:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/keynuker /var/cache/keynuker 2>/dev/null || true


FROM scratch
COPY --from=upstream /keynuker /keynuker
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/keynuker /var/log/keynuker
COPY --from=builder /var/cache/keynuker /var/cache/keynuker

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="keynuker"       org.opencontainers.image.description="KeyNuker - key detection"       org.opencontainers.image.vendor="clonezilla"       org.opencontainers.image.source="https://github.com/clonezilla/keynuker"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
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
ENTRYPOINT ["/keynuker"]

CMD ["--help"]
