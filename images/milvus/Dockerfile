ARG VERSION=v2.6.15
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM milvusdb/milvus:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION=2.4.0
RUN apk add --no-cache wget ca-certificates
COPY --from=upstream /milvus /opt/milvus
RUN adduser -u 65532 -D milvus 2>/dev/null || true && \
    mkdir -p /app /var/log/milvus /var/cache/milvus && chown -R milvus:milvus /app /var/log/milvus /var/cache/milvus /opt/milvus 2>/dev/null || true
WORKDIR /app

EXPOSE 19530
EXPOSE 9101

LABEL org.opencontainers.image.title="milvus" org.opencontainers.image.version="2.4.0" org.opencontainers.image.vendor="Milvus" evergreen.image.tier="2" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi" \
      org.opencontainers.image.source="https://github.com/milvus-io/milvus" \
      org.opencontainers.image.description="milvus container image" \
evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:19530/ || exit 1
ENTRYPOINT ["/opt/milvus/bin/milvus"]
