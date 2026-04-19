# =============================================================================
# SOVEREIGN HARDENED MONGODB
# Generated from template - Version: 7.0.11
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.0.11
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends mongodb-org ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' mongodb 2>/dev/null || true
RUN mkdir -p /app /var/log/mongod /var/cache/mongod && chown -R mongodb:mongodb /app /var/log/mongod /var/cache/mongod 2>/dev/null || true
USER mongodb
WORKDIR /app
EXPOSE 27017
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD mongod mongosh --eval db.adminCommand('ping')
ENTRYPOINT ["mongod"]
LABEL org.opencontainers.image.title="mongodb" \
      org.opencontainers.image.version="7.0.11" \
      org.opencontainers.image.vendor="MongoDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
