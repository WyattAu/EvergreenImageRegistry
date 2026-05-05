ARG VERSION=latest

FROM selfhostedpro/yacht:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/yacht /var/cache/yacht 2>/dev/null || true


FROM scratch
COPY --from=upstream /app/yacht /usr/local/bin/yacht
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/yacht /var/log/yacht
COPY --from=builder /var/cache/yacht /var/cache/yacht

WORKDIR /app

EXPOSE 9101

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE

LABEL org.opencontainers.image.description="yacht container image" \
      org.opencontainers.image.source="https://github.com/SelfhostedPro/Yacht" \
            org.opencontainers.image.version="latest"

ENTRYPOINT ["/yacht"]

CMD ["--help"]
