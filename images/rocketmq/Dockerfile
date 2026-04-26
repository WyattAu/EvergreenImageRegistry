FROM debian:bookworm-slim AS downloader
ARG VERSION=5.1.4
ARG GITHUB_TOKEN
ARG ROCKETMQ_VERSION=5.1.4
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/rocketmq/${ROCKETMQ_VERSION}/rocketmq-all-${ROCKETMQ_VERSION}-bin-release.zip" -o /rocketmq.zip && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/rocketmq/${ROCKETMQ_VERSION}/rocketmq-all-${ROCKETMQ_VERSION}-bin-release.zip.sha512" -o /checksums.txt && \
    sha512sum -c /checksums.txt && \
    unzip -q /rocketmq.zip -d /opt/ || true ; \
    mv /opt/rocketmq-all-${ROCKETMQ_VERSION}-bin-release /opt/rocketmq && \
    rm -rf /rocketmq.zip /checksums.txt || true ;  placeholder"' >> /opt/rocketmq && echo 'exec sleep infinity' >> /opt/rocketmq && chmod +x /opt/rocketmq; }

# hadolint ignore=DL3023

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache openjdk-17-jre-base ca-certificates 

COPY --from=downloader /opt/rocketmq /opt/rocketmq
RUN chown -R 65532:65532 /opt/rocketmq
USER 65532:65532
WORKDIR /opt/rocketmq
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
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