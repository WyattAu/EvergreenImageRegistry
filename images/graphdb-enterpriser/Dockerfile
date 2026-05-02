ARG VERSION=latest

FROM ontotext/graphdb:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates
RUN adduser -D -u 65532 -s /bin/false graphdb 2>/dev/null || true
RUN mkdir -p /var/lib/graphdb /var/log/graphdb /var/cache/graphdb /opt/graphdb/home /opt 2>/dev/null || true
COPY --from=upstream /opt/graphdb /opt/graphdb
RUN chown -R 65532:65532 /opt/graphdb /var/lib/graphdb /var/log/graphdb /var/cache/graphdb 2>/dev/null || true

WORKDIR /opt/graphdb

EXPOSE 7200
EXPOSE 9101

LABEL org.opencontainers.image.title="graphdb-enterpriser" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Sovereign hardened GraphDB Enterprise - semantic graph database" org.opencontainers.image.vendor="Ontotext" sovereign.image.tier="1" sovereign.image.category="database" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/opt/graphdb/bin/graphdb"]
