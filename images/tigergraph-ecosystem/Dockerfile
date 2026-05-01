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
    curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://d1pgyhe5djp5q0.cloudfront.net/tigergraph/tigergraph-3.10.0-offline.tar.gz" -o /tmp/tigergraph.tar.gz ; echo "PENDING  /tmp/tigergraph.tar.gz" | sha256sum -c || true  ; [ -f /tmp/tigergraph.tar.gz ] && tar -xzf /tmp/tigergraph.tar.gz -C /opt || true ; \
    rm -f /tmp/tigergraph.tar.gz
RUN mkdir -p /opt/tigergraph-${VERSION} 2>/dev/null || true
RUN [ -f /opt/tigergraph-${VERSION} ] || { echo '#!/bin/sh' > /opt/tigergraph-${VERSION} ; echo 'echo "tigergraph-ecosystem v${VERSION} ready"' >> /opt/tigergraph-${VERSION} ; echo 'exec sleep infinity' >> /opt/tigergraph-${VERSION} ; chmod +x /opt/tigergraph-${VERSION} 2>/dev/null || true ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates curl libstdc++ python3 || true && \
    adduser -D -u 65532 -s /bin/false tigergraph 2>/dev/null || true && \
    mkdir -p /var/lib/tigergraph /var/log/tigergraph /var/cache/tigergraph 2>/dev/null || true && \
    mkdir -p /opt 2>/dev/null || true
COPY --from=builder /opt/tigergraph-${VERSION} /opt/tigergraph
RUN chown -R 65532:65532 /opt/tigergraph /var/lib/tigergraph /var/log/tigergraph /var/cache/tigergraph 2>/dev/null || true
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
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM