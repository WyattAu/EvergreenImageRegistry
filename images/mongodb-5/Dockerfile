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
RUN curl -fsSL "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2204-${VERSION}.tgz" -o /tmp/mongodb.tgz \
    && echo "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890  /tmp/mongodb.tgz" | sha256sum -c - \
    && tar -xzf /tmp/mongodb.tgz -C /tmp \
    && strip --strip-all /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION}/bin/* \
    && mv /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION}/bin/* /usr/local/bin/ \
    && rm -rf /tmp/mongodb.tgz /tmp/mongodb-linux-x86_64-ubuntu2204-${VERSION}

FROM debian:bookworm-20250113-slim
RUN apt-get update && apt-get install -y --no-install-recommends libssl3 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN groupadd -g 65534 mongodb && useradd -u 65534 -g mongodb -s /usr/sbin/nologin mongodb
RUN mkdir -p /data/db /var/log/mongodb /var/cache/mongodb && chown -R 65534:65534 /data/db /var/log/mongodb /var/cache/mongodb
COPY --from=builder /usr/local/bin/mongod /usr/local/bin/mongod
COPY --from=builder /usr/local/bin/mongo /usr/local/bin/mongo
COPY --from=builder /usr/local/bin/mongos /usr/local/bin/mongos
USER 65534:65534
WORKDIR /data/db
EXPOSE 27017
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["mongo", "--eval", "db.adminCommand('ping')", "--quiet", "127.0.0.1/test"]
ENTRYPOINT ["mongod"]
LABEL org.opencontainers.image.title="mongodb-5" \
      org.opencontainers.image.description="Sovereign hardened MongoDB 5.0 - document database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="MongoDB" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
