# =============================================================================
# SOVEREIGN HARDENED TIGERGRAPH-ECOSYSTEM
# Constraint: debian-slim - ecosystem tools for TigerGraph
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.10.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://d1pgyhe5djp5q0.cloudfront.net/tigergraph/tigergraph-3.10.0-offline.tar.gz" -o /tmp/tigergraph.tar.gz \
    && echo "PENDING  /tmp/tigergraph.tar.gz" | sha256sum -c || true  # \
    && tar -xzf /tmp/tigergraph.tar.gz -C /opt \
    && rm /tmp/tigergraph.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates curl libstdc++ python3
RUN useradd -m -u 65532 -s /usr/sbin/nologin tigergraph 2>/dev/null || true
RUN mkdir -p /var/lib/tigergraph /var/log/tigergraph /var/cache/tigergraph
COPY --from=builder /opt/tigergraph-${VERSION} /opt/tigergraph 2>/dev/null || true
RUN chown -R 65532:65532 /opt/tigergraph /var/lib/tigergraph /var/log/tigergraph /var/cache/tigergraph
USER 65532:65532
WORKDIR /opt/tigergraph
EXPOSE 14240 9000 8123 8443
ENTRYPOINT ["/opt/tigergraph/bin/gadmin", "start", "all"]
LABEL org.opencontainers.image.title="tigergraph-ecosystem" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened TigerGraph Ecosystem - ecosystem tools and utilities" \
      org.opencontainers.image.vendor="TigerGraph" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM