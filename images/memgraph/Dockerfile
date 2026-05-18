ARG VERSION=3.9.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM memgraph/memgraph:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION=3.9.0
RUN apk add --no-cache ca-certificates python3 && \
    adduser -u 65532 -s /bin/false memgraph 2>/dev/null || true && \
    mkdir -p /var/lib/memgraph /var/log/memgraph /var/cache/memgraph /etc/memgraph 2>/dev/null || true && \
    mkdir -p /opt 2>/dev/null || true
COPY --from=upstream /usr/lib/memgraph/memgraph /opt/memgraph/bin/memgraph
RUN chown -R 65532:65532 /opt/memgraph /var/lib/memgraph /var/log/memgraph /var/cache/memgraph /etc/memgraph 2>/dev/null || true

WORKDIR /var/lib/memgraph

EXPOSE 7687 7444
EXPOSE 9101

LABEL org.opencontainers.image.title="memgraph" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Evergreen hardened Memgraph - in-memory graph database" org.opencontainers.image.vendor="Memgraph" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi" \
      org.opencontainers.image.source="https://github.com/memgraph/memgraph"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:7444/ || exit 1
ENTRYPOINT ["/opt/memgraph/bin/memgraph", "--data-directory=/var/lib/memgraph"]
