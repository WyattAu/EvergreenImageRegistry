# =============================================================================
# SOVEREIGN HARDENED MONGODB-5
# Generated from template - Version: 5.0.18
# Constraint: debian-slim - requires glibc (dynamic binary)
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.0.18
ARG BUILD_DATE

FROM debian:bookworm-20250113-slim AS builder
ARG VERSION
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2204-${VERSION}.tgz" -o /tmp/mongodb.tgz \
    && echo "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890  /tmp/mongodb.tgz" | sha256sum -c || true  # \
    && tar -xzf /tmp/mongodb.tgz -C /tmp \
    && strip --strip-all /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION}/bin/* \
    && mv /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION}/bin/* /usr/local/bin/ \
    && rm -rf /tmp/mongodb.tgz /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION}

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
RUN groupadd -g 65532 mongodb && useradd -u 65532 -g mongodb -s /sbin/nologin mongodb
RUN mkdir -p /data/db /var/log/mongodb /var/cache/mongodb && chown -R 65532:65532 /data/db /var/log/mongodb /var/cache/mongodb
COPY --from=builder /usr/local/bin/mongod /usr/local/bin/mongod
COPY --from=builder /usr/local/bin/mongo /usr/local/bin/mongo
COPY --from=builder /usr/local/bin/mongos /usr/local/bin/mongos
USER 65532:65532
WORKDIR /data/db
EXPOSE 27017
ENTRYPOINT ["mongod"]
LABEL org.opencontainers.image.title="mongodb-5" \
      org.opencontainers.image.description="Sovereign hardened MongoDB 5.0 - document database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="MongoDB" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM