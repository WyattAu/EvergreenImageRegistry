ARG VERSION=latest

FROM rethinkdb/rethinkdb:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates libstdc++
RUN adduser -u 65532 -s /bin/false rethinkdb || true
RUN mkdir -p /var/lib/rethinkdb /var/log/rethinkdb /var/cache/rethinkdb /data /opt 2>/dev/null || true
COPY --from=upstream /rethinkdb /opt/rethinkdb
RUN chown -R 65532:65532 /opt/rethinkdb /var/lib/rethinkdb /var/log/rethinkdb /var/cache/rethinkdb /data

WORKDIR /data

EXPOSE 28015 29015 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="rethinkdb" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Sovereign hardened RethinkDB - real-time NoSQL database" org.opencontainers.image.vendor="RethinkDB" sovereign.image.tier="1" sovereign.image.category="database" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/opt/rethinkdb/bin/rethinkdb", "--bind", "all", "--directory", "/data"]
