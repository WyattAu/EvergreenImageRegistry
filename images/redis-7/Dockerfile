# =============================================================================
# SOVEREIGN HARDENED REDIS-7
# Generated from template - Version: 7.4.1
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.4.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65534 -s /usr/sbin/nologin redis 2>/dev/null || true
RUN mkdir -p /app /var/log/redis-server /var/cache/redis-server

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    redis-server ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove apt apt-get dpkg 2>/dev/null || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/redis-server /var/log/redis-server
COPY --from=builder --chown=65534:65534 /var/cache/redis-server /var/cache/redis-server
USER 65534:65534
WORKDIR /app
EXPOSE 6379
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD redis-cli -h localhost ping
ENTRYPOINT ["redis-server"]
LABEL org.opencontainers.image.title="redis-7" \
      org.opencontainers.image.version="7.4.1" \
      org.opencontainers.image.vendor="Redis" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.hardened="true"
