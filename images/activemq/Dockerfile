# =============================================================================
# SOVEREIGN HARDENED ACTIVEMQ (Classic)
# Apache ActiveMQ Classic message broker
# Constraint: debian-slim - Java runtime requires glibc + JDK
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG ACTIVEMQ_VERSION=5.18.3
ARG JAVA_VERSION=17
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://archive.apache.org/dist/activemq/${ACTIVEMQ_VERSION}/apache-activemq-${ACTIVEMQ_VERSION}-bin.tar.gz" -o /activemq.tar.gz && \
    curl -fsSL "https://archive.apache.org/dist/activemq/${ACTIVEMQ_VERSION}/apache-activemq-${ACTIVEMQ_VERSION}-bin.tar.gz.sha512" -o /checksums.txt && \
    sha512sum -c /checksums.txt && \
    tar -xzf /activemq.tar.gz -C /opt/ && \
    mv /opt/apache-activemq-${ACTIVEMQ_VERSION} /opt/activemq && \
    rm -rf /activemq.tar.gz /checksums.txt

# hadolint ignore=DL3023
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-${JAVA_VERSION}-jre-headless ca-certificates && rm -rf /var/lib/apt/lists/* && \
    groupadd -g 65534 activemq && useradd -u 65534 -g activemq -s /usr/sbin/nologin -d /opt/activemq activemq

COPY --from=downloader /opt/activemq /opt/activemq
RUN chown -R 65534:65534 /opt/activemq

USER 65534:65534
WORKDIR /opt/activemq
ENV JAVA_HOME="/usr/lib/jvm/java-${JAVA_VERSION}-openjdk-amd64"
ENV ACTIVEMQ_HOME="/opt/activemq"
EXPOSE 61616 8161 5672 61613
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-fsSL", "http://localhost:8161/api/health"]
ENTRYPOINT ["/opt/activemq/bin/activemq", "console"]
LABEL org.opencontainers.image.title="activemq" \
      org.opencontainers.image.version="5.18.3" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.source="https://github.com/apache/activemq" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distrole="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
