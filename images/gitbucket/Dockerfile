ARG VERSION=4.40.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/gitbucket/gitbucket/releases/download/${VERSION}/gitbucket.war" -o /tmp/gitbucket.war && \
    echo "7e124543a48f3d349b2e93dddbaace1a7122a18b1a11b0e6ab403f0645d646d5  /tmp/gitbucket.war" | sha256sum -c

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /shim
RUN chmod +x /shim
RUN apk add --no-cache ca-certificates openjdk-21-jdk-headless && \
    addgroup -S -g 10000 gitbucket 2>/dev/null || true && \
    adduser -u 65532 -G gitbucket -D -h /opt/gitbucket -s /bin/false gitbucket && \
    mkdir -p /opt/gitbucket /var/log/gitbucket /var/data/gitbucket && \
    chown -R 65532:65532 /opt/gitbucket /var/log/gitbucket /var/data/gitbucket
COPY --from=builder /tmp/gitbucket.war /opt/gitbucket/gitbucket.war
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
ENV GITBUCKET_HOME="/var/data/gitbucket"
WORKDIR /opt/gitbucket
EXPOSE 8080
LABEL org.opencontainers.image.title="gitbucket" \
      org.opencontainers.image.description="GitBucket - Scala-based Git platform" \
      org.opencontainers.image.version="4.40.0" \
      org.opencontainers.image.vendor="GitBucket" \
      org.opencontainers.image.source="https://github.com/gitbucket/gitbucket" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]
ENTRYPOINT ["/shim", "run"]
