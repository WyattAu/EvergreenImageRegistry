ARG VERSION=latest

FROM zincsearch/zincsearch:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/zincone /var/cache/zincone 2>/dev/null || true


FROM scratch
COPY --from=upstream /go/bin/zincsearch /usr/local/bin/zincone
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/zincone /var/log/zincone
COPY --from=builder /var/cache/zincone /var/cache/zincone

WORKDIR /tmp

EXPOSE 4080
EXPOSE 9101

LABEL org.opencontainers.image.title="zincone" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Sovereign hardened ZincOne - ZincSearch observability edition" org.opencontainers.image.vendor="ZincSearch" sovereign.image.tier="1" sovereign.image.category="database" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/usr/local/bin/zincone"]
