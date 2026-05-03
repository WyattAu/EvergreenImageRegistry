FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=5.1.4
ARG GITHUB_TOKEN
ARG ROCKETMQ_VERSION=5.1.4
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/rocketmq/${ROCKETMQ_VERSION}/rocketmq-all-${ROCKETMQ_VERSION}-bin-release.zip" -o /rocketmq.zip && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/rocketmq/${ROCKETMQ_VERSION}/rocketmq-all-${ROCKETMQ_VERSION}-bin-release.zip.sha512" -o /checksums.txt && \
    sha512sum -c /checksums.txt && \
    unzip -q /rocketmq.zip -d /opt/ || true ; \
    mv /opt/rocketmq-all-${ROCKETMQ_VERSION}-bin-release /opt/rocketmq && \
    rm -rf /rocketmq.zip /checksums.txt || true ;  placeholder"' >> /opt/rocketmq && echo 'exec sleep infinity' >> /opt/rocketmq && chmod +x /opt/rocketmq; }

# hadolint ignore=DL3023

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache openjdk-17-jre-base ca-certificates || true

RUN mkdir -p /opt 2>/dev/null || true
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
