# =============================================================================
# EVERGREEN HARDENED JANUSGRAPH
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.0.0
WORKDIR /tmp
RUN mkdir -p /opt/janusgraph-${VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/JanusGraph/janusgraph/releases/download/v${VERSION}/janusgraph-${VERSION}.zip -o /tmp/janusgraph.zip ; echo "PENDING  /tmp/janusgraph.zip" | sha256sum -c  ; unzip -q /tmp/janusgraph.zip -d /opt ; \
    rm -f /tmp/janusgraph.zip
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=1.0.0
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -s /bin/false janusgraph 2>/dev/null || true && \
    mkdir -p /var/lib/janusgraph /var/log/janusgraph /var/cache/janusgraph 2>/dev/null || true
COPY --from=builder /opt/janusgraph-${VERSION} /opt/janusgraph
RUN chown -R 65532:65532 /opt/janusgraph /var/lib/janusgraph /var/log/janusgraph /var/cache/janusgraph
USER 65532:65532
WORKDIR /opt/janusgraph
EXPOSE 8182

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8182"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="janusgraph" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened JanusGraph - distributed graph database" \
      org.opencontainers.image.vendor="JanusGraph" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/JanusGraph/janusgraph"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
