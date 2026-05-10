ARG VERSION=24.09.05

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=24.09.05
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/apache/ofbiz-framework/archive/refs/tags/release${VERSION}.tar.gz" \
    -o /apache-ofbiz.tar.gz && \
    tar -xzf /apache-ofbiz.tar.gz -C /opt/ && rm -f /apache-ofbiz.tar.gz
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates curl
COPY --from=downloader /opt/ /opt/apache-ofbiz
RUN mkdir -p /app /var/log/apache-ofbiz && \
    chown -R 65532:65532 /app /var/log/apache-ofbiz /opt/apache-ofbiz
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["java", "-jar", "/opt/apache-ofbiz/apache-ofbiz"]
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
