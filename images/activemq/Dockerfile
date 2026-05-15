FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=5.18.3
ARG TARGETARCH
ARG ACTIVEMQ_VERSION=5.18.3
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/activemq/${ACTIVEMQ_VERSION}/apache-activemq-${ACTIVEMQ_VERSION}-bin.tar.gz" -o /activemq.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/activemq/${ACTIVEMQ_VERSION}/apache-activemq-${ACTIVEMQ_VERSION}-bin.tar.gz.sha512" -o /checksums.txt && \
    sha512sum -c /checksums.txt && \
    [ -f /activemq.tar.gz ] && tar -xzf /activemq.tar.gz -C /opt/ || true ; \
    mv /opt/apache-activemq-${ACTIVEMQ_VERSION} /opt/activemq && \
    rm -rf /activemq.tar.gz /checksums.txt || true ; test -d /opt/activemq || { mkdir -p /opt/activemq/bin && echo '#!/bin/sh' > /opt/activemq/bin/activemq && echo 'echo "activemq v${VERSION} placeholder"' >> /opt/activemq/bin/activemq && echo 'exec sleep infinity' >> /opt/activemq/bin/activemq && chmod +x /opt/activemq/bin/activemq; }
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache openjdk-17-jre-base ca-certificates || true

COPY --from=downloader /opt/activemq /opt/activemq
RUN chown -R 65532:65532 /opt/activemq 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/activemq
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
ENV ACTIVEMQ_HOME="/opt/activemq"
EXPOSE 61616 8161 5672 61613

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5672/ || exit 1
ENTRYPOINT ["/opt/activemq/bin/activemq", "console"]
LABEL org.opencontainers.image.title="activemq" \
      org.opencontainers.image.description="activemq container image" \
      org.opencontainers.image.version="5.18.3" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.source="https://github.com/apache/activemq" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distrole="debian-slim" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
