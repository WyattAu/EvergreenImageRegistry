ARG VERSION=5.0

FROM mongo:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

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

LABEL org.opencontainers.image.title="mongodb-5" org.opencontainers.image.description="Sovereign hardened MongoDB 5.0 - document database" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.vendor="MongoDB" sovereign.image.status="functional" sovereign.image.tier="1" sovereign.image.category="database" sovereign.constraint.nonroot="true" sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["mongod"]
