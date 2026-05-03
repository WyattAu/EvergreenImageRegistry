ARG VERSION=latest

FROM michenriksen/gitrob:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/gitrob /var/cache/gitrob 2>/dev/null || true


FROM scratch
COPY --from=upstream /gitrob /gitrob
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/gitrob /var/log/gitrob
COPY --from=builder /var/cache/gitrob /var/cache/gitrob

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="gitrob"       org.opencontainers.image.description="GitRob - sensitive file finder"       org.opencontainers.image.vendor="michenriksen"       org.opencontainers.image.source="https://github.com/michenriksen/gitrob"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true"
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
ENTRYPOINT ["/gitrob"]

CMD ["--help"]
