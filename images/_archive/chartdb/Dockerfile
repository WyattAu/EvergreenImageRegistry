ARG VERSION=v1.20.1
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL -L \
        "https://github.com/chartdb/chartdb/releases/download/${VERSION}/chartdb-${VERSION}-linux-x64.jar" \
        -o /tmp/chartdb.jar

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim
RUN apk add --no-cache ca-certificates java-21-default-jdk && \
    adduser -D -u 65532 -s /bin/false chartdb 2>/dev/null || true && \
    mkdir -p /var/lib/chartdb /var/log/chartdb /var/cache/chartdb /opt/chartdb 2>/dev/null || true
COPY --from=downloader /tmp/chartdb.jar /opt/chartdb/chartdb.jar
RUN chown -R 65532:65532 /opt/chartdb /var/lib/chartdb /var/log/chartdb /var/cache/chartdb 2>/dev/null || true
WORKDIR /opt/chartdb
EXPOSE 8080 9101
LABEL org.opencontainers.image.title="chartdb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened ChartDB - database schema visualization tool" \
      org.opencontainers.image.vendor="ChartDB" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
      org.opencontainers.image.source="https://github.com/chartdb/chartdb"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "java -jar /opt/chartdb/chartdb.jar"]
