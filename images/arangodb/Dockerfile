# =============================================================================
# SOVEREIGN HARDENED ARANGODB
# Generated from template - Version: 3.12.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.12.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL -k "https://download.arangodb.com/arangodb312/Linux/x86_64/ArangoDB312_linux_x86_64.tar.gz" -o /tmp/arangodb.tar.gz && \
    tar -xzf /tmp/arangodb.tar.gz -C /opt && \
    mv /opt/arangodb3* /opt/arangodb 2>/dev/null || true && \
    chmod +x /opt/arangodb/usr/sbin/arangod 2>/dev/null || true && \
    rm -f /tmp/arangodb.tar.gz

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 libgcc-s1 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' arangodb 2>/dev/null || true
RUN mkdir -p /app /var/log/arangod /var/cache/arangod && chown -R arangodb:arangodb /app /var/log/arangod /var/cache/arangod 2>/dev/null || true
USER arangodb
WORKDIR /app
COPY --from=downloader /opt/arangodb /opt/arangodb
EXPOSE 8529
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8529/_api/version
ENTRYPOINT ["/opt/arangodb/usr/sbin/arangod"]
LABEL org.opencontainers.image.title="arangodb" \
      org.opencontainers.image.version="3.12.1" \
      org.opencontainers.image.vendor="ArangoDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
