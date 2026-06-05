ARG VERSION=24.09.05
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=24.09.05
RUN mkdir -p /opt/ || true
RUN mkdir -p /opt/ || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/apache/ofbiz-framework/archive/refs/tags/release${VERSION}.tar.gz" \
    -o /apache-ofbiz.tar.gz && \
    tar -xzf /apache-ofbiz.tar.gz -C /opt/ && rm -f /apache-ofbiz.tar.gz
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl
COPY --from=downloader /opt/ /opt/apache-ofbiz
RUN mkdir -p /app /var/log/apache-ofbiz && \
    chown -R 65532:65532 /app /var/log/apache-ofbiz /opt/apache-ofbiz
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="apache-ofbiz" \
      org.opencontainers.image.description="apache-ofbiz container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Apache OFBiz" \
      org.opencontainers.image.source="https://github.com/apache/ofbiz-framework" \
      evergreen.image.tier="2" \
      evergreen.image.category="crm-erp" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
