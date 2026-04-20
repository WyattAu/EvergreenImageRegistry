# =============================================================================
# SOVEREIGN HARDENED ARANGODB
# Generated from template - Version: 3.12.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.12.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg2 && \
    curl -fsSL https://download.arangodb.com/arangodb312/Release/Linux/Debian_12/Release.key | gpg --dearmor -o /usr/share/keyrings/arangodb.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/arangodb.gpg] https://download.arangodb.com/arangodb312/Release/Linux/Debian_12/ /" > /etc/apt/sources.list.d/arangodb.list && \
    apt-get update && apt-get install -y --no-install-recommends arangodb3 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' arangodb 2>/dev/null || true
RUN mkdir -p /app /var/log/arangod /var/cache/arangod && chown -R arangodb:arangodb /app /var/log/arangod /var/cache/arangod 2>/dev/null || true
USER arangodb
WORKDIR /app
EXPOSE 8529
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8529/_api/version
ENTRYPOINT ["arangod"]
LABEL org.opencontainers.image.title="arangodb" \
      org.opencontainers.image.version="3.12.1" \
      org.opencontainers.image.vendor="ArangoDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
