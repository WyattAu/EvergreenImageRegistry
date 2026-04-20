# =============================================================================
# SOVEREIGN HARDENED COUCHBASE
# Generated from template - Version: 7.6.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.6.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg2 wget && \
    wget -qO- https://packages.couchbase.com/ubuntu/couchbase.key | gpg --dearmor -o /usr/share/keyrings/couchbase.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/couchbase.gpg] https://packages.couchbase.com/debian jammy jammy/main" > /etc/apt/sources.list.d/couchbase.list && \
    apt-get update && apt-get install -y --no-install-recommends couchbase-server && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' couchbase 2>/dev/null || true
RUN mkdir -p /app /var/log/couchbase-server /var/cache/couchbase-server && chown -R couchbase:couchbase /app /var/log/couchbase-server /var/cache/couchbase-server 2>/dev/null || true
USER couchbase
WORKDIR /app
EXPOSE 8091 11210
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8091/pools
ENTRYPOINT ["couchbase-server"]
LABEL org.opencontainers.image.title="couchbase" \
      org.opencontainers.image.version="7.6.1" \
      org.opencontainers.image.vendor="Couchbase" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
