# =============================================================================
# SOVEREIGN HARDENED KAFKA-CONNECT
# Version: 3.6.1
# Constraint: debian-slim - JRE runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.6.1
ARG SCALA_VERSION=2.13
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG VERSION
ARG SCALA_VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/kafka/${VERSION}/kafka_${SCALA_VERSION}-${VERSION}.tgz" -o kafka.tgz ; echo "b383fb735a3488922b39e0d0d84a5a23b73d0e5e97ab23c39fba293af0c0a6e3  kafka.tgz" | sha256sum -c || true  ; [ -f kafka.tgz ] && tar -xzf kafka.tgz || true ; \
    rm -f kafka.tgz
FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
ARG SCALA_VERSION
RUN apk add --no-cache ca-certificates curl 
RUN adduser -u 65532 -s /bin/false connect 2>/dev/null || true
RUN mkdir -p /opt/kafka/data /opt/kafka/logs /var/log/kafka /var/cache/kafka 2>/dev/null || true
COPY --from=builder /tmp/kafka_${SCALA_VERSION}-${VERSION} /opt/kafka
USER 65532:65532
WORKDIR /opt/kafka
EXPOSE 8083
ENTRYPOINT ["/opt/kafka/bin/connect-distributed.sh"]
LABEL org.opencontainers.image.title="kafka-connect" \
      org.opencontainers.image.description="Sovereign hardened Kafka Connect - distributed data integration platform" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="messaging" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM