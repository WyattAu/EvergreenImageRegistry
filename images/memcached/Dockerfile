# =============================================================================
# SOVEREIGN HARDENED MEMCACHED
# Generated from template - Version: 1.6.26
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.6.26
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65534 -s /usr/sbin/nologin memcached 2>/dev/null || true
RUN mkdir -p /app /var/log/memcached /var/cache/memcached

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    memcached ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove apt apt-get dpkg 2>/dev/null || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/memcached /var/log/memcached
COPY --from=builder --chown=65534:65534 /var/cache/memcached /var/cache/memcached
USER 65534:65534
WORKDIR /app
EXPOSE 11211
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/bin/memcached", "--version"]
ENTRYPOINT ["memcached"]
LABEL org.opencontainers.image.title="memcached" \
      org.opencontainers.image.version="1.6.26" \
      org.opencontainers.image.vendor="Memcached" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.hardened="true"
