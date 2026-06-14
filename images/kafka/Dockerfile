# =============================================================================
# EVERGREEN HARDENED KAFKA
# Generated from template - Version: 3.6.1
# Constraint: wolfi-base — Java JRE runtime required
# =============================================================================

ARG VERSION=3.6.1
ARG TARGETARCH
ARG SCALA_VERSION=2.13
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=3.6.1
ARG SCALA_VERSION
WORKDIR /tmp
RUN mkdir -p /tmp/kafka_${SCALA_VERSION}-${VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/kafka/${VERSION}/kafka_${SCALA_VERSION}-${VERSION}.tgz" -o kafka.tgz ; echo "b383fb735a3488922b39e0d0d84a5a23b73d0e5e97ab23c39fba293af0c0a6e3  kafka.tgz" | sha256sum -c  ; [ -f kafka.tgz ] && tar -xzf kafka.tgz ; \
    rm -f kafka.tgz

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=3.6.1
ARG SCALA_VERSION
RUN apk add --no-cache ca-certificates bash && \
    adduser -u 65532 -s /bin/false kafka 2>/dev/null || true && \
    mkdir -p /kafka/data /kafka/log 2>/dev/null || true
COPY --from=builder /tmp/kafka_${SCALA_VERSION}-${VERSION} /opt/kafka
USER 65532:65532
WORKDIR /opt/kafka
ENV SHIM_METRICS_ENABLED="true" \
    SHIM_HEALTHCHECK_TYPE="http" \
    SHIM_HEALTHCHECK_URL="http://localhost:8082/health"
EXPOSE 9092

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--http", "http://127.0.0.1:8082/health"]

ENTRYPOINT ["/shim", "run", "-c", "kafka-server-start.sh"]
CMD ["-c", "/opt/kafka/bin/kafka-server-start.sh"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="messaging" \
      org.opencontainers.image.title="kafka" \
      org.opencontainers.image.description="Evergreen hardened Apache Kafka - distributed event streaming platform" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.source="https://github.com/apache/kafka"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"

EXPOSE 9101
STOPSIGNAL SIGTERM
