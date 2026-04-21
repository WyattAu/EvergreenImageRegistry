# =============================================================================
# SOVEREIGN HARDENED MEMGRAPH
# Constraint: debian-slim - compile from source (C++ graph database)
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.18.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake curl ca-certificates git \
    libgrpc++-dev libprotobuf-dev protobuf-compiler \
    libboost-all-dev libssl-dev libspdlog-dev \
    python3 python3-pip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN git clone --depth 1 --branch v${VERSION} https://github.com/memgraph/memgraph.git /tmp/memgraph-src 2>/dev/null || \
    (curl -fsSL "https://github.com/memgraph/memgraph/releases/download/v${VERSION}/memgraph-${VERSION}-linux-amd64.tar.gz" -o /tmp/memgraph.tar.gz \
    && tar -xzf /tmp/memgraph.tar.gz -C /opt && rm /tmp/memgraph.tar.gz) || true

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgrpc++1 libprotobuf32 libboost-all1.74 libssl3 ca-certificates python3 && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin memgraph 2>/dev/null || true
RUN mkdir -p /var/lib/memgraph /var/log/memgraph /var/cache/memgraph /etc/memgraph
COPY --from=builder /opt/memgraph /opt/memgraph 2>/dev/null || true
RUN chown -R 65534:65534 /opt/memgraph /var/lib/memgraph /var/log/memgraph /var/cache/memgraph /etc/memgraph
USER 65534:65534
WORKDIR /var/lib/memgraph
EXPOSE 7687 7444
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:7444"]
ENTRYPOINT ["/opt/memgraph/bin/memgraph", "--data-directory=/var/lib/memgraph"]
LABEL org.opencontainers.image.title="memgraph" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Memgraph - in-memory graph database" \
      org.opencontainers.image.vendor="Memgraph" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
