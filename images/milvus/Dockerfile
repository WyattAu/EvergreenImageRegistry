# =============================================================================
# SOVEREIGN HARDENED MILVUS
# Generated from template - Version: 2.4.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.4.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/milvus-io/milvus/releases/download/v${VERSION}/milvus-standalone_${VERSION}_linux_amd64.tar.gz" -o /tmp/milvus.tar.gz && \
    tar -xzf /tmp/milvus.tar.gz -C /opt && rm /tmp/milvus.tar.gz && \
    chmod +x /opt/milvus/bin/milvus 2>/dev/null || true
RUN useradd -m -u 65534 -g '' milvus 2>/dev/null || true
RUN mkdir -p /app /var/log/milvus /var/cache/milvus && chown -R milvus:milvus /app /var/log/milvus /var/cache/milvus /opt/milvus 2>/dev/null || true
USER milvus
WORKDIR /app
EXPOSE 19530
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:9091/healthz
ENTRYPOINT ["/opt/milvus/bin/milvus"]
LABEL org.opencontainers.image.title="milvus" \
      org.opencontainers.image.version="2.4.0" \
      org.opencontainers.image.vendor="Milvus" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
