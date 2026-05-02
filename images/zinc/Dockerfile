ARG VERSION=latest

FROM zincsearch/zincsearch:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/zinc /var/cache/zinc 2>/dev/null || true


FROM scratch
COPY --from=upstream /go/bin/zincsearch /usr/local/bin/zincsearch
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/zinc /var/log/zinc
COPY --from=builder /var/cache/zinc /var/cache/zinc

WORKDIR /tmp

EXPOSE 4080
EXPOSE 9101

LABEL org.opencontainers.image.title="zinc" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Sovereign hardened ZincSearch - lightweight alternative to Elasticsearch" org.opencontainers.image.vendor="ZincSearch" sovereign.image.tier="1" sovereign.image.category="database" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/usr/local/bin/zincsearch"]
