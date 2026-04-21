# =============================================================================
# SOVEREIGN HARDENED OPENSEARCH
# Generated from template - Version: 2.14.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.14.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL -k "https://artifacts.opensearch.org/releases/bundle/opensearch/${VERSION}/opensearch-${VERSION}-linux-x64.tar.gz" -o /tmp/opensearch.tar.gz && \
    tar -xzf /tmp/opensearch.tar.gz -C /opt && \
    mv /opt/opensearch-${VERSION} /opt/opensearch && \
    rm -f /tmp/opensearch.tar.gz

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates java11-runtime-headless 2>/dev/null || \
    apt-get install -y --no-install-recommends default-jre-headless && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' opensearch 2>/dev/null || true
RUN mkdir -p /app /var/log/opensearch /var/cache/opensearch && chown -R opensearch:opensearch /app /var/log/opensearch /var/cache/opensearch 2>/dev/null || true
USER opensearch
WORKDIR /app
COPY --from=downloader /opt/opensearch /opt/opensearch
EXPOSE 9200 9300
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:9200
ENTRYPOINT ["/opt/opensearch/bin/opensearch"]
LABEL org.opencontainers.image.title="opensearch" \
      org.opencontainers.image.version="2.14.0" \
      org.opencontainers.image.vendor="OpenSearch" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
