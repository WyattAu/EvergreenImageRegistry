FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31 AS builder
ARG VERSION=2.5.0
RUN apk add --no-cache curl ca-certificates || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://fastdl.mongodb.org/tools/mongodb-mongosh/${VERSION}/mongosh-${VERSION}-linux-x64.tgz" \
    -o /tmp/mongosh.tgz && \
    mkdir -p /opt/mongosh && \
    tar -xzf /tmp/mongosh.tgz -C /opt/mongosh --strip-components=1 && \
    rm -f /tmp/mongosh.tgz || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=2.5.0
RUN apk add --no-cache ca-certificates || true && \
    addgroup -S -g 10000 mongosh 2>/dev/null || true && \
    adduser -u 65532 -G mongosh -D -h /app -s /bin/false mongosh 2>/dev/null || true && \
    mkdir -p /app /var/log/mongosh 2>/dev/null || true
COPY --from=builder /opt/mongosh /opt/mongosh
RUN chown -R 65532:65532 /app /var/log/mongosh 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV PATH="/opt/mongosh/bin:${PATH}"
EXPOSE 27017

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD echo "db.runCommand({ping:1})" | mongosh --quiet
ENTRYPOINT ["/opt/mongosh/bin/mongosh"]
LABEL org.opencontainers.image.title="mongodb-opsmanager" \
      org.opencontainers.image.description="MongoDB Ops Manager - mongosh CLI tool" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="MongoDB" \
      org.opencontainers.image.source="https://www.mongodb.com/docs/mongodb-shell/" \
      evergreen.image.tier="2" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
