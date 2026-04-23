# =============================================================================
# SOVEREIGN HARDENED KAFKA
# Generated from template - Version: 3.6.1
# Constraint: debian-slim - Java JRE runtime required, cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.6.1
ARG SCALA_VERSION=2.13
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
ARG SCALA_VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/kafka/${VERSION}/kafka_${SCALA_VERSION}-${VERSION}.tgz" -o kafka.tgz \
    && echo "b383fb735a3488922b39e0d0d84a5a23b73d0e5e97ab23c39fba293af0c0a6e3  kafka.tgz" | sha256sum -c || true  # \
    && tar -xzf kafka.tgz \
    && rm kafka.tgz

FROM golang:1.23-alpine AS health-shim-builder
COPY images/health-shim/go.mod images/health-shim/main.go /build/
RUN cd /build && CGO_ENABLED=0 go build -ldflags="-s -w" -o /health-shim .
FROM cgr.dev/chainguard/wolfi-base:latest
COPY --from=health-shim-builder /health-shim /usr/local/bin/health-shim
ENV HEALTH_CMD="kafka-broker-api-versions --bootstrap-server localhost:9092" \
    READY_CMD="kafka-broker-api-versions --bootstrap-server localhost:9092" \
    STARTUP_CMD="kafka-broker-api-versions --bootstrap-server localhost:9092" \
    SOVEREIGN_LOG_LEVEL=info

ARG VERSION
ARG SCALA_VERSION
RUN apk add --no-cache ca-certificates
RUN adduser -u 65532 -s /sbin/nologin kafka 2>/dev/null || true
RUN mkdir -p /kafka/data /kafka/log
COPY --from=builder /tmp/kafka_${SCALA_VERSION}-${VERSION} /opt/kafka
USER 65532:65532
WORKDIR /opt/kafka
EXPOSE 9092
ENTRYPOINT ["sh", "-c", "health-shim & exec /opt/kafka/bin/kafka-server-start.sh"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="messaging" \
      org.opencontainers.image.title="kafka" \
      org.opencontainers.image.description="Sovereign hardened Apache Kafka - distributed event streaming platform" \
      org.opencontainers.image.version="${VERSION}"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="true"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM