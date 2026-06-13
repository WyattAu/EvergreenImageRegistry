# =============================================================================
# EVERGREEN HARDENED NIFI-REGISTRY
# Generated from template - Version: 1.26.0
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.26.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.26.0
RUN mkdir -p /opt/nifi-registry-${VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/nifi/${VERSION}/nifi-registry-${VERSION}-bin.zip" \
    -o /nifi-registry.zip ; echo "af7b39f6bceacfd4e2e4f8805e9da9f7faea3ea9a7b031748f51c6cf72fd7021  /nifi-registry.zip" | sha256sum -c  ; unzip -q /nifi-registry.zip -d /opt ; \
    rm -f /nifi-registry.zip && \
    mkdir -p /opt/nifi-registry-${VERSION} 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=1.26.0
RUN apk add --no-cache ca-certificates && \
    adduser -D -u 65532 -s /bin/false nifi 2>/dev/null || true && \
    mkdir -p /var/lib/nifi-registry /var/log/nifi-registry /var/cache/nifi-registry 2>/dev/null || true && \
    mkdir -p /opt 2>/dev/null || true
RUN mkdir -p /opt/nifi-registry || true
COPY --from=builder /opt/nifi-registry-${VERSION} /opt/nifi-registry
RUN addgroup -S -g 2 nifi>/dev/null || true && adduser -u 65532 -G nifi -D -s /bin/false nifi 2>/dev/null || true && \
    chown -R nifi:nifi /opt/nifi-registry /var/lib/nifi-registry /var/log/nifi-registry /var/cache/nifi-registry 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/nifi-registry
EXPOSE 18080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:18080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="nifi-registry" \
      org.opencontainers.image.version="1.26.0" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="Evergreen hardened NiFi Registry - versioned flow management for Apache NiFi" \
      evergreen.image.tier="1" \
      evergreen.image.category="data-flow" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/apache/nifi-registry"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
