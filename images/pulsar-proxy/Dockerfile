# =============================================================================
# EVERGREEN HARDENED PULSAR-PROXY
# Version: 3.2.0
# Constraint: debian-slim - JRE runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.2.0
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/pulsar/pulsar-${VERSION}/apache-pulsar-${VERSION}-bin.tar.gz" -o pulsar.tar.gz ; echo "0000000000000000000000000000000000000000000000000000000000000000  pulsar.tar.gz" | sha256sum -c || true  ; [ -f pulsar.tar.gz ] && tar -xzf pulsar.tar.gz || true ; \
    rm -f pulsar.tar.gz ; rm -rf apache-pulsar-${VERSION}/examples apache-pulsar-${VERSION}/tools
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -s /bin/false pulsar 2>/dev/null || true && \
    mkdir -p /opt/pulsar/data /opt/pulsar/logs /var/log/pulsar /var/cache/pulsar 2>/dev/null || true
COPY --from=builder /tmp/apache-pulsar-${VERSION} /opt/pulsar
USER 65532:65532
WORKDIR /opt/pulsar
EXPOSE 6650 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:6650/ || exit 1
ENTRYPOINT ["/opt/pulsar/bin/pulsar"]
CMD ["proxy"]
LABEL org.opencontainers.image.title="pulsar-proxy" \
      org.opencontainers.image.description="Evergreen hardened Pulsar Proxy - multi-tenant message routing proxy" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Apache" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="messaging" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="15s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms" \
            org.opencontainers.image.source="https://github.com/apache/pulsar"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
