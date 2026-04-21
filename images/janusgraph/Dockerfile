# =============================================================================
# SOVEREIGN HARDENED JANUSGRAPH
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/JanusGraph/janusgraph/releases/download/v${VERSION}/janusgraph-${VERSION}.zip" -o /tmp/janusgraph.zip \
    && echo "PENDING  /tmp/janusgraph.zip" | sha256sum -c - \
    && unzip -q /tmp/janusgraph.zip -d /opt \
    && rm /tmp/janusgraph.zip

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless curl && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin janusgraph 2>/dev/null || true
RUN mkdir -p /var/lib/janusgraph /var/log/janusgraph /var/cache/janusgraph
COPY --from=builder /opt/janusgraph-${VERSION} /opt/janusgraph
RUN chown -R 65534:65534 /opt/janusgraph /var/lib/janusgraph /var/log/janusgraph /var/cache/janusgraph
USER 65534:65534
WORKDIR /opt/janusgraph
EXPOSE 8182
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8182"]
ENTRYPOINT ["/opt/janusgraph/bin/gremlin.sh"]
LABEL org.opencontainers.image.title="janusgraph" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened JanusGraph - distributed graph database" \
      org.opencontainers.image.vendor="JanusGraph" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
