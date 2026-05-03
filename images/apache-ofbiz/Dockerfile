ARG VERSION=24.09.05

FROM debian:bookworm-slim AS downloader
ARG VERSION
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/apache/ofbiz-framework/archive/refs/tags/release${VERSION}.tar.gz" \
    -o /apache-ofbiz.tar.gz && \
    tar -xzf /apache-ofbiz.tar.gz -C /opt/ && rm -f /apache-ofbiz.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl
COPY --from=downloader /opt/ /opt/apache-ofbiz 2>/dev/null || true
RUN mkdir -p /app /var/log/apache-ofbiz && \
    chown -R 65532:65532 /app /var/log/apache-ofbiz /opt/apache-ofbiz
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/opt/apache-ofbiz/apache-ofbiz"]
LABEL org.opencontainers.image.title="apache-ofbiz" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Apache OFBiz" \
      org.opencontainers.image.source="https://github.com/apache/ofbiz-framework" \
      sovereign.image.tier="2" \
      sovereign.image.category="crm-erp" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
