ARG VERSION=latest

FROM realm/mongodb-realm:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates curl || true && \
    adduser -D -u 65532 -s /bin/false realm 2>/dev/null || true && \
    mkdir -p /var/lib/realm /var/log/realm /var/cache/realm /opt 2>/dev/null || true
COPY --from=upstream /realm /opt/realm
RUN chown -R 65532:65532 /opt/realm /var/lib/realm /var/log/realm /var/cache/realm 2>/dev/null || true

WORKDIR /opt/realm

EXPOSE 9090
EXPOSE 9101

LABEL org.opencontainers.image.title="realm-server" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Sovereign hardened MongoDB Realm Server - application backend platform" org.opencontainers.image.vendor="MongoDB" sovereign.image.tier="1" sovereign.image.category="database" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/opt/realm/bin/realm-server"]
