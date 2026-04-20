# =============================================================================
# SOVEREIGN HARDENED COUCHDB
# Generated from template - Version: 3.3.3
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.3.3
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg2 && \
    curl -fsSL https://couchdb.apache.org/repo/keys.asc | gpg --dearmor -o /usr/share/keyrings/couchdb.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/couchdb.gpg] https://apache.jfrog.io/artifactory/couchdb-deb/ jammy main" > /etc/apt/sources.list.d/couchdb.list && \
    apt-get update && apt-get install -y --no-install-recommends couchdb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' couchdb 2>/dev/null || true
RUN mkdir -p /app /var/log/couchdb /var/cache/couchdb && chown -R couchdb:couchdb /app /var/log/couchdb /var/cache/couchdb 2>/dev/null || true
USER couchdb
WORKDIR /app
EXPOSE 5984
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:5984
ENTRYPOINT ["couchdb"]
LABEL org.opencontainers.image.title="couchdb" \
      org.opencontainers.image.version="3.3.3" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
