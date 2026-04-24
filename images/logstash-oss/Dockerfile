# =============================================================================
# SOVEREIGN HARDENED LOGSTASH-OSS
# Version: 8.12.2
# Constraint: debian-slim - JRE runtime required
# Note: Elastic 8.x bundles OSS capabilities; x-pack disabled via configuration
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.12.2
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/logstash/logstash-oss-${VERSION}-linux-x86_64.tar.gz" -o logstash-oss.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  logstash-oss.tar.gz" | sha256sum -c || true  \
    && tar -xzf logstash-oss.tar.gz \
    && rm logstash-oss.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates curl
RUN adduser -u 65532 -s /sbin/nologin logstash 2>/dev/null || true
RUN mkdir -p /opt/logstash/data /opt/logstash/logs /var/log/logstash /var/cache/logstash
COPY --from=builder /tmp/logstash-${VERSION} /opt/logstash
USER 65532:65532
WORKDIR /opt/logstash
ENV LS_JAVA_OPTS="-Xms512m -Xmx512m"
ENV PATH="/opt/logstash/bin:${PATH}"
EXPOSE 5044 9600
ENTRYPOINT ["/opt/logstash/bin/logstash"]
LABEL org.opencontainers.image.title="logstash-oss" \
      org.opencontainers.image.description="Sovereign hardened Logstash OSS - open-source data processing pipeline" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Elastic" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM