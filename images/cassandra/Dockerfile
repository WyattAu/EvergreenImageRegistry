# =============================================================================
# SOVEREIGN HARDENED CASSANDRA
# Generated from template - Version: 4.1.4
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.1.4
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends cassandra ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' cassandra 2>/dev/null || true
RUN mkdir -p /app /var/log/cassandra /var/cache/cassandra && chown -R cassandra:cassandra /app /var/log/cassandra /var/cache/cassandra 2>/dev/null || true
USER cassandra
WORKDIR /app
EXPOSE 7000 7001 9042
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD cassandra nodetool status
ENTRYPOINT ["cassandra"]
LABEL org.opencontainers.image.title="cassandra" \
      org.opencontainers.image.version="4.1.4" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
