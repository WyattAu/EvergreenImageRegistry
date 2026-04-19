# =============================================================================
# SOVEREIGN HARDENED SCYLLADB
# Generated from template - Version: 5.4.6
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.4.6
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends scylla ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' scylla 2>/dev/null || true
RUN mkdir -p /app /var/log/scylla /var/cache/scylla && chown -R scylla:scylla /app /var/log/scylla /var/cache/scylla 2>/dev/null || true
USER scylla
WORKDIR /app
EXPOSE 7000 9042
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD nodetool status
ENTRYPOINT ["scylla"]
LABEL org.opencontainers.image.title="scylladb" \
      org.opencontainers.image.version="5.4.6" \
      org.opencontainers.image.vendor="ScyllaDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
