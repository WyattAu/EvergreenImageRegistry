# =============================================================================
# SOVEREIGN HARDENED APACHE ROCKETMQ
# Apache RocketMQ distributed messaging platform
# Constraint: debian-slim - Java runtime requires glibc + JDK
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG ROCKETMQ_VERSION=5.1.4
ARG JAVA_VERSION=17
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://archive.apache.org/dist/rocketmq/${ROCKETMQ_VERSION}/rocketmq-all-${ROCKETMQ_VERSION}-bin-release.zip" -o /rocketmq.zip && \
    curl -fsSL "https://archive.apache.org/dist/rocketmq/${ROCKETMQ_VERSION}/rocketmq-all-${ROCKETMQ_VERSION}-bin-release.zip.sha512" -o /checksums.txt && \
    sha512sum -c /checksums.txt && \
    unzip -q /rocketmq.zip -d /opt/ && \
    mv /opt/rocketmq-all-${ROCKETMQ_VERSION}-bin-release /opt/rocketmq && \
    rm -rf /rocketmq.zip /checksums.txt

# hadolint ignore=DL3023
FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache openjdk-${JAVA_VERSION}-jre-headless ca-certificates

COPY --from=downloader /opt/rocketmq /opt/rocketmq
RUN chown -R 65532:65532 /opt/rocketmq

USER 65532:65532
WORKDIR /opt/rocketmq
ENV JAVA_HOME="/usr/lib/jvm/java-${JAVA_VERSION}-openjdk-amd64"
ENV ROCKETMQ_HOME="/opt/rocketmq"
EXPOSE 9876 10911 10909
ENTRYPOINT ["/opt/rocketmq/bin/mqnamesrv"]
LABEL org.opencontainers.image.title="rocketmq" \
      org.opencontainers.image.version="5.1.4" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.source="https://github.com/apache/rocketmq" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distrole="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM