ARG VERSION=latest

FROM michenriksen/gitrob:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/gitrob /var/cache/gitrob 2>/dev/null || true


FROM scratch
COPY --from=upstream /gitrob /gitrob
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/gitrob /var/log/gitrob
COPY --from=builder /var/cache/gitrob /var/cache/gitrob

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="gitrob"       org.opencontainers.image.description="GitRob - sensitive file finder"       org.opencontainers.image.vendor="michenriksen"       org.opencontainers.image.source="https://github.com/michenriksen/gitrob"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/gitrob"]

CMD ["--help"]
