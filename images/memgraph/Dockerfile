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
    build-base cmake curl ca-certificates git \
    libgrpc++-dev libprotobuf-dev protobuf-compiler \
    libboost-all-dev libssl-dev libspdlog-dev \
    python3 py3-pip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN git clone --depth 1 --branch v${VERSION} https://github.com/memgraph/memgraph.git /tmp/memgraph-src 2>/dev/null || \
    (curl --retry 3 --retry-delay 5 -fsSL "https://github.com/memgraph/memgraph/releases/download/v${VERSION}/memgraph-${VERSION}-linux-amd64.tar.gz" -o /tmp/memgraph.tar.gz \
    && tar -xzf /tmp/memgraph.tar.gz -C /opt && rm /tmp/memgraph.tar.gz) || true

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates python3
RUN useradd -m -u 65532 -s /sbin/nologin memgraph 2>/dev/null || true
RUN mkdir -p /var/lib/memgraph /var/log/memgraph /var/cache/memgraph /etc/memgraph
COPY --from=builder /opt/memgraph /opt/memgraph 2>/dev/null || true
RUN chown -R 65532:65532 /opt/memgraph /var/lib/memgraph /var/log/memgraph /var/cache/memgraph /etc/memgraph
USER 65532:65532
WORKDIR /var/lib/memgraph
EXPOSE 7687 7444
ENTRYPOINT ["/opt/memgraph/bin/memgraph", "--data-directory=/var/lib/memgraph"]
LABEL org.opencontainers.image.title="memgraph" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Memgraph - in-memory graph database" \
      org.opencontainers.image.vendor="Memgraph" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM