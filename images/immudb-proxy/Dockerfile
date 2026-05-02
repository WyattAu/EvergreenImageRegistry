ARG VERSION=latest

FROM ghcr.io/codenotary/immudb:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/immudb-proxy /var/cache/immudb-proxy 2>/dev/null || true


FROM scratch
COPY --from=upstream /usr/local/bin/immudb-proxy /usr/local/bin/immudb-proxy
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/immudb-proxy /var/log/immudb-proxy
COPY --from=builder /var/cache/immudb-proxy /var/cache/immudb-proxy

EXPOSE 3323
EXPOSE 9101

LABEL org.opencontainers.image.title="immudb-proxy" org.opencontainers.image.description="Sovereign hardened immudb-proxy - proxy mode for immudb" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.vendor="Codenotary" sovereign.image.status="functional" sovereign.image.tier="1" sovereign.image.category="security" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/usr/local/bin/immudb-proxy"]
