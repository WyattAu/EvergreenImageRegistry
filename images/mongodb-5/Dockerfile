ARG VERSION=5.0

FROM mongo:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION=5.0.18
RUN apk add --no-cache ca-certificates
RUN addgroup -S -g 65532 mongodb && adduser -u 65532 -G mongodb -D -s /bin/false mongodb || true
RUN mkdir -p /data/db /var/log/mongodb /var/cache/mongodb && chown -R 65532:65532 /data/db /var/log/mongodb /var/cache/mongodb 2>/dev/null || true
RUN mkdir -p /usr/local/bin 2>/dev/null || true
COPY --from=upstream /usr/bin/mongod /usr/local/bin/mongod
COPY --from=upstream /usr/bin/mongo /usr/local/bin/mongo
COPY --from=upstream /usr/bin/mongos /usr/local/bin/mongos

WORKDIR /data/db

EXPOSE 27017
EXPOSE 9101

LABEL org.opencontainers.image.title="mongodb-5" org.opencontainers.image.description="Evergreen hardened MongoDB 5.0 - document database" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.vendor="MongoDB" evergreen.image.status="functional" evergreen.image.tier="1" evergreen.image.category="database" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD mongosh --quiet --eval "db.runCommand({ping:1})"
ENTRYPOINT ["mongod"]
