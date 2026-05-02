ARG VERSION=latest

FROM memgraph/memgraph:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates python3
RUN adduser -u 65532 -s /bin/false memgraph 2>/dev/null || true
RUN mkdir -p /var/lib/memgraph /var/log/memgraph /var/cache/memgraph /etc/memgraph 2>/dev/null || true
RUN mkdir -p /opt 2>/dev/null || true
COPY --from=upstream /usr/lib/memgraph/memgraph /opt/memgraph/bin/memgraph
RUN chown -R 65532:65532 /opt/memgraph /var/lib/memgraph /var/log/memgraph /var/cache/memgraph /etc/memgraph 2>/dev/null || true

WORKDIR /var/lib/memgraph

EXPOSE 7687 7444
EXPOSE 9101

LABEL org.opencontainers.image.title="memgraph" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Sovereign hardened Memgraph - in-memory graph database" org.opencontainers.image.vendor="Memgraph" sovereign.image.tier="1" sovereign.image.category="database" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/opt/memgraph/bin/memgraph", "--data-directory=/var/lib/memgraph"]
