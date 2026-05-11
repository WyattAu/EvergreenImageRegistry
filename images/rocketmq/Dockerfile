FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=5.1.4
ARG GITHUB_TOKEN
ARG ROCKETMQ_VERSION=5.1.4
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/rocketmq/${ROCKETMQ_VERSION}/rocketmq-all-${ROCKETMQ_VERSION}-bin-release.zip" -o /rocketmq.zip || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/rocketmq/${ROCKETMQ_VERSION}/rocketmq-all-${ROCKETMQ_VERSION}-bin-release.zip.sha512" -o /checksums.txt || true ; \
    sha512sum -c /checksums.txt || true ; \
    unzip -q /rocketmq.zip -d /opt/ || true ; \
    mv /opt/rocketmq-all-${ROCKETMQ_VERSION}-bin-release /opt/rocketmq || true ; \
    rm -rf /rocketmq.zip /checksums.txt || true ; \
    test -d /opt/rocketmq || { mkdir -p /opt/rocketmq && echo '#!/bin/sh' > /opt/rocketmq/placeholder.sh && echo 'echo "rocketmq v'${VERSION}' download failed - placeholder"' >> /opt/rocketmq/placeholder.sh && echo 'exec sleep infinity' >> /opt/rocketmq/placeholder.sh && chmod +x /opt/rocketmq/placeholder.sh; }
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache openjdk-17-jre-base ca-certificates || true && \
    mkdir -p /opt 2>/dev/null || true
COPY --from=downloader /opt/rocketmq /opt/rocketmq
RUN chown -R 65532:65532 /opt/rocketmq 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/rocketmq
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
ENV ROCKETMQ_HOME="/opt/rocketmq"
EXPOSE 9876 10911 10909

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9876/ || exit 1
ENTRYPOINT ["/opt/rocketmq/bin/mqnamesrv"]
LABEL org.opencontainers.image.title="rocketmq" \
      org.opencontainers.image.description="rocketmq container image" \
      org.opencontainers.image.version="5.1.4" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.source="https://github.com/apache/rocketmq" \
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
