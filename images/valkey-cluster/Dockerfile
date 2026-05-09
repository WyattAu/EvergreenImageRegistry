ARG VERSION=8.0.1

FROM valkey/valkey:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION=7.2.4
RUN apk add --no-cache ca-certificates
COPY --from=upstream /usr/local/bin/valkey-server /usr/local/bin/valkey-server
RUN adduser -u 65532 -s /bin/false valkey 2>/dev/null || true && \
    mkdir -p /app /var/log/valkey-cluster /var/cache/valkey-cluster /var/lib/valkey ; \
    chown -R 65532:65532 /app /var/log/valkey-cluster /var/cache/valkey-cluster /var/lib/valkey


WORKDIR /app

EXPOSE 6379 16379
EXPOSE 9101

LABEL org.opencontainers.image.title="valkey-cluster" org.opencontainers.image.version="7.2.4" org.opencontainers.image.description="Valkey in Cluster Mode - Distributed Key-Value Store" org.opencontainers.image.vendor="Valkey" org.opencontainers.image.source="https://github.com/valkey-io/valkey" evergreen.image.tier="1" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:6379/ || exit 1
ENTRYPOINT ["valkey", "--cluster-enabled", "yes", \