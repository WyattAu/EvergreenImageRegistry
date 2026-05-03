ARG VERSION=latest

FROM ontotext/graphdb-free:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
RUN apk add --no-cache ca-certificates
RUN adduser -D -u 65532 -s /bin/false graphdb 2>/dev/null || true
RUN mkdir -p /var/lib/graphdb /var/log/graphdb /var/cache/graphdb /opt/graphdb/home /opt 2>/dev/null || true
COPY --from=upstream /opt/graphdb /opt/graphdb
RUN chown -R 65532:65532 /opt/graphdb /var/lib/graphdb /var/log/graphdb /var/cache/graphdb 2>/dev/null || true

WORKDIR /opt/graphdb

EXPOSE 7200
EXPOSE 9101

LABEL org.opencontainers.image.title="graphdb-free" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Evergreen hardened GraphDB Free - semantic graph database" org.opencontainers.image.vendor="Ontotext" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:7200/ || exit 1
ENTRYPOINT ["/opt/graphdb/bin/graphdb"]
