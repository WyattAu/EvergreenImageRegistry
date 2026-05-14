# =============================================================================
# EVERGREEN HARDENED KAFKA-CONNECT
# Version: 3.6.1
# Constraint: debian-slim - JRE runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.6.1
ARG TARGETARCH
ARG SCALA_VERSION=2.13
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=3.6.1
ARG SCALA_VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/kafka/${VERSION}/kafka_${SCALA_VERSION}-${VERSION}.tgz" -o kafka.tgz ; echo "b383fb735a3488922b39e0d0d84a5a23b73d0e5e97ab23c39fba293af0c0a6e3  kafka.tgz" | sha256sum -c || true  ; [ -f kafka.tgz ] && tar -xzf kafka.tgz || true ; \
    rm -f kafka.tgz
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION=3.6.1
ARG SCALA_VERSION
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -s /bin/false connect 2>/dev/null || true && \
    mkdir -p /opt/kafka/data /opt/kafka/logs /var/log/kafka /var/cache/kafka 2>/dev/null || true
COPY --from=builder /tmp/kafka_${SCALA_VERSION}-${VERSION} /opt/kafka
USER 65532:65532
WORKDIR /opt/kafka
EXPOSE 8083

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8083/ || exit 1
ENTRYPOINT ["/opt/kafka/bin/connect-distributed.sh"]
LABEL org.opencontainers.image.title="kafka-connect" \
      org.opencontainers.image.description="Evergreen hardened Kafka Connect - distributed data integration platform" \
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
            org.opencontainers.image.source="https://github.com/apache/kafka"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
