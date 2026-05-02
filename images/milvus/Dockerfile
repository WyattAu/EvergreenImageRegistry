ARG VERSION=latest

FROM milvusdb/milvus:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION=2.4.0
RUN apk add --no-cache curl ca-certificates
COPY --from=upstream /milvus /opt/milvus
RUN adduser -u 65532 -D milvus 2>/dev/null || true
RUN mkdir -p /app /var/log/milvus /var/cache/milvus && chown -R milvus:milvus /app /var/log/milvus /var/cache/milvus /opt/milvus 2>/dev/null || true

WORKDIR /app

EXPOSE 19530
EXPOSE 9101

LABEL org.opencontainers.image.title="milvus" org.opencontainers.image.version="2.4.0" org.opencontainers.image.vendor="Milvus" sovereign.image.tier="2" sovereign.constraint.nonroot="true" sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/opt/milvus/bin/milvus"]
