# =============================================================================
# SOVEREIGN HARDENED MONGODB-6
# Generated from template - Version: 6.0.14
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=6.0.14
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65534 -s /usr/sbin/nologin mongodb 2>/dev/null || true
RUN mkdir -p /app /var/log/mongod /var/cache/mongod

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    mongodb-org ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove apt apt-get dpkg 2>/dev/null || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/mongod /var/log/mongod
COPY --from=builder --chown=65534:65534 /var/cache/mongod /var/cache/mongod
USER 65534:65534
WORKDIR /app
EXPOSE 27017
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD mongosh --eval "db.adminCommand('ping')" --quiet 127.0.0.1/test
ENTRYPOINT ["mongod"]
LABEL org.opencontainers.image.title="mongodb-6" \
      org.opencontainers.image.version="6.0.14" \
      org.opencontainers.image.vendor="MongoDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.hardened="true"
