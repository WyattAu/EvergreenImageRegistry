# =============================================================================
# SOVEREIGN HARDENED GRAPHDB-FREE
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=10.7.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/ontotext/graphdb/releases/download/v${VERSION}/graphdb-free-${VERSION}-dist.zip" -o /tmp/graphdb.zip \
    && echo "PENDING  /tmp/graphdb.zip" | sha256sum -c - \
    && unzip -q /tmp/graphdb.zip -d /opt \
    && rm /tmp/graphdb.zip

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin graphdb 2>/dev/null || true
RUN mkdir -p /var/lib/graphdb /var/log/graphdb /var/cache/graphdb /opt/graphdb/home
COPY --from=builder /opt/graphdb-free-${VERSION} /opt/graphdb
RUN chown -R 65534:65534 /opt/graphdb /var/lib/graphdb /var/log/graphdb /var/cache/graphdb
USER 65534:65534
WORKDIR /opt/graphdb
EXPOSE 7200
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-f", "http://localhost:7200/rest/repositories"]
ENTRYPOINT ["/opt/graphdb/bin/graphdb"]
LABEL org.opencontainers.image.title="graphdb-free" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened GraphDB Free - semantic graph database" \
      org.opencontainers.image.vendor="Ontotext" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
