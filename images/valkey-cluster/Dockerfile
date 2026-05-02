ARG VERSION=latest

FROM valkey/valkey:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION=7.2.4
RUN apk add --no-cache ca-certificates
COPY --from=upstream /usr/local/bin/valkey-server /usr/local/bin/valkey-server
RUN adduser -u 65532 -s /bin/false valkey 2>/dev/null || true && \
    mkdir -p /app /var/log/valkey-cluster /var/cache/valkey-cluster /var/lib/valkey ; \
    chown -R 65532:65532 /app /var/log/valkey-cluster /var/cache/valkey-cluster /var/lib/valkey


WORKDIR /app

EXPOSE 6379 16379
EXPOSE 9101

LABEL org.opencontainers.image.title="valkey-cluster" org.opencontainers.image.version="7.2.4" org.opencontainers.image.description="Valkey in Cluster Mode - Distributed Key-Value Store" org.opencontainers.image.vendor="Valkey" org.opencontainers.image.source="https://github.com/valkey-io/valkey" sovereign.image.tier="1" sovereign.constraint.nonroot="true" sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["valkey", "--cluster-enabled", "yes", \
