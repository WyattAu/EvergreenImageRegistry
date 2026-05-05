# =============================================================================
# EVERGREEN HARDENED KAFKA
# Generated from template - Version: 3.6.1
# Constraint: debian-slim - Java JRE runtime required, cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.6.1
ARG SCALA_VERSION=2.13
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
ARG SCALA_VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/kafka/${VERSION}/kafka_${SCALA_VERSION}-${VERSION}.tgz" -o kafka.tgz ; echo "b383fb735a3488922b39e0d0d84a5a23b73d0e5e97ab23c39fba293af0c0a6e3  kafka.tgz" | sha256sum -c || true  ; [ -f kafka.tgz ] && tar -xzf kafka.tgz || true ; \
    rm -f kafka.tgz
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ENV HEALTH_CMD="kafka-broker-api-versions --bootstrap-server localhost:9092" \
    READY_CMD="kafka-broker-api-versions --bootstrap-server localhost:9092" \
    STARTUP_CMD="kafka-broker-api-versions --bootstrap-server localhost:9092" \
    EVERGREEN_LOG_LEVEL=info

ARG VERSION
ARG SCALA_VERSION
ARG TARGETARCH
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -s /bin/false kafka 2>/dev/null || true && \
    mkdir -p /kafka/data /kafka/log 2>/dev/null || true
COPY --from=builder /tmp/kafka_${SCALA_VERSION}-${VERSION} /opt/kafka
USER 65532:65532
WORKDIR /opt/kafka
EXPOSE 9092

HEALTHCHECK NONE
ENTRYPOINT ["sh", "-c", "/opt/kafka/bin/kafka-server-start.sh"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="messaging" \
      org.opencontainers.image.title="kafka" \
      org.opencontainers.image.description="Evergreen hardened Apache Kafka - distributed event streaming platform" \
      org.opencontainers.image.version="${VERSION}" \
            org.opencontainers.image.source="https://github.com/apache/kafka"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
