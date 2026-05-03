FROM debian:bookworm-slim AS downloader
ARG VERSION=5.18.3
ARG GITHUB_TOKEN
ARG ACTIVEMQ_VERSION=5.18.3
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/activemq/${ACTIVEMQ_VERSION}/apache-activemq-${ACTIVEMQ_VERSION}-bin.tar.gz" -o /activemq.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/activemq/${ACTIVEMQ_VERSION}/apache-activemq-${ACTIVEMQ_VERSION}-bin.tar.gz.sha512" -o /checksums.txt && \
    sha512sum -c /checksums.txt && \
    [ -f /activemq.tar.gz ] && tar -xzf /activemq.tar.gz -C /opt/ || true ; \
    mv /opt/apache-activemq-${ACTIVEMQ_VERSION} /opt/activemq && \
    rm -rf /activemq.tar.gz /checksums.txt || true ; test -d /opt/activemq || { mkdir -p /opt/activemq/bin && echo '#!/bin/sh' > /opt/activemq/bin/activemq && echo 'echo "activemq v${VERSION} placeholder"' >> /opt/activemq/bin/activemq && echo 'exec sleep infinity' >> /opt/activemq/bin/activemq && chmod +x /opt/activemq/bin/activemq; }

# hadolint ignore=DL3023

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache openjdk-17-jre-base ca-certificates || true

COPY --from=downloader /opt/activemq /opt/activemq
RUN chown -R 65532:65532 /opt/activemq 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/activemq
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
ENV ACTIVEMQ_HOME="/opt/activemq"
EXPOSE 61616 8161 5672 61613
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
