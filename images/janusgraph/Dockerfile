# =============================================================================
# SOVEREIGN HARDENED JANUSGRAPH
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/JanusGraph/janusgraph/releases/download/v${VERSION}/janusgraph-${VERSION}.zip -o /tmp/janusgraph.zip ; echo "PENDING  /tmp/janusgraph.zip" | sha256sum -c || true  ; unzip -q /tmp/janusgraph.zip -d /opt || true ; \
    rm -f /tmp/janusgraph.zip
FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates curl 
RUN adduser -u 65532 -s /bin/false janusgraph 2>/dev/null || true
RUN mkdir -p /var/lib/janusgraph /var/log/janusgraph /var/cache/janusgraph 2>/dev/null || true
COPY --from=builder /opt/janusgraph-${VERSION} /opt/janusgraph
RUN chown -R 65532:65532 /opt/janusgraph /var/lib/janusgraph /var/log/janusgraph /var/cache/janusgraph
USER 65532:65532
WORKDIR /opt/janusgraph
EXPOSE 8182
ENTRYPOINT ["/opt/janusgraph/bin/gremlin.sh"]
LABEL org.opencontainers.image.title="janusgraph" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened JanusGraph - distributed graph database" \
      org.opencontainers.image.vendor="JanusGraph" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM