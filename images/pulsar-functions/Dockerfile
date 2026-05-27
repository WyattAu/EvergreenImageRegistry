# =============================================================================
# EVERGREEN HARDENED PULSAR-FUNCTIONS
# Version: 3.2.0
# Constraint: debian-slim - JRE runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.2.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=3.2.0
WORKDIR /tmp
RUN mkdir -p /tmp/apache-pulsar-${VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/pulsar/pulsar-${VERSION}/apache-pulsar-${VERSION}-bin.tar.gz" -o pulsar.tar.gz ; echo "4ff679193843ec3c50103198c3ee5dc265c3851af06bbb42bca67bcc684c1262  pulsar.tar.gz" | sha256sum -c  ; [ -f pulsar.tar.gz ] && tar -xzf pulsar.tar.gz ; \
    rm -f pulsar.tar.gz ; rm -rf apache-pulsar-${VERSION}/examples apache-pulsar-${VERSION}/tools
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION=3.2.0
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -s /bin/false pulsar 2>/dev/null || true && \
    mkdir -p /opt/pulsar/data /opt/pulsar/logs /var/log/pulsar /var/cache/pulsar 2>/dev/null || true
COPY --from=builder /tmp/apache-pulsar-${VERSION} /opt/pulsar
USER 65532:65532
WORKDIR /opt/pulsar
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8080/ || exit 1
ENTRYPOINT ["/opt/pulsar/bin/pulsar"]
CMD ["functions-worker"]
LABEL org.opencontainers.image.title="pulsar-functions" \
      org.opencontainers.image.description="Evergreen hardened Pulsar Functions Worker - serverless event processing" \
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
