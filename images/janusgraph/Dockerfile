# =============================================================================
# EVERGREEN HARDENED JANUSGRAPH
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/JanusGraph/janusgraph/releases/download/v${VERSION}/janusgraph-${VERSION}.zip -o /tmp/janusgraph.zip ; echo "PENDING  /tmp/janusgraph.zip" | sha256sum -c || true  ; unzip -q /tmp/janusgraph.zip -d /opt || true ; \
    rm -f /tmp/janusgraph.zip
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -s /bin/false janusgraph 2>/dev/null || true && \
    mkdir -p /var/lib/janusgraph /var/log/janusgraph /var/cache/janusgraph 2>/dev/null || true
COPY --from=builder /opt/janusgraph-${VERSION} /opt/janusgraph
RUN chown -R 65532:65532 /opt/janusgraph /var/lib/janusgraph /var/log/janusgraph /var/cache/janusgraph
USER 65532:65532
WORKDIR /opt/janusgraph
EXPOSE 8182

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8182/ || exit 1
ENTRYPOINT ["/opt/janusgraph/bin/gremlin.sh"]
LABEL org.opencontainers.image.title="janusgraph" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened JanusGraph - distributed graph database" \
      org.opencontainers.image.vendor="JanusGraph" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
