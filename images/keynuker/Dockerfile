ARG VERSION=latest

FROM ghcr.io/clonezilla/keynuker:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/keynuker /var/cache/keynuker 2>/dev/null || true


FROM scratch
COPY --from=upstream /keynuker /keynuker
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/keynuker /var/log/keynuker
COPY --from=builder /var/cache/keynuker /var/cache/keynuker

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="keynuker"       org.opencontainers.image.description="KeyNuker - key detection"       org.opencontainers.image.vendor="clonezilla"       org.opencontainers.image.source="https://github.com/clonezilla/keynuker"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/keynuker"]

CMD ["--help"]
