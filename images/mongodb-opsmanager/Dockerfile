FROM cgr.dev/chainguard/wolfi-base:latest AS builder
ARG VERSION=2.5.0
RUN apk add --no-cache curl ca-certificates || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://fastdl.mongodb.org/tools/mongodb-mongosh/${VERSION}/mongosh-${VERSION}-linux-x64.tgz" \
    -o /tmp/mongosh.tgz && \
    mkdir -p /opt/mongosh && \
    tar -xzf /tmp/mongosh.tgz -C /opt/mongosh --strip-components=1 && \
    rm /tmp/mongosh.tgz || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=2.5.0
RUN apk add --no-cache ca-certificates || true
RUN addgroup -S -g 10000 mongosh 2>/dev/null || true && \
    adduser -u 65532 -G mongosh -D -h /app -s /bin/false mongosh 2>/dev/null || true
RUN mkdir -p /app /var/log/mongosh 2>/dev/null || true
COPY --from=builder /opt/mongosh /opt/mongosh
RUN chown -R 65532:65532 /app /var/log/mongosh 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV PATH="/opt/mongosh/bin:${PATH}"
EXPOSE 27017
ENTRYPOINT ["/opt/mongosh/bin/mongosh"]
LABEL org.opencontainers.image.title="mongodb-opsmanager" \
      org.opencontainers.image.description="MongoDB Ops Manager - mongosh CLI tool" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="MongoDB" \
      org.opencontainers.image.source="https://www.mongodb.com/docs/mongodb-shell/" \
      sovereign.image.tier="2" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="tcp"
EXPOSE 9101
STOPSIGNAL SIGTERM
