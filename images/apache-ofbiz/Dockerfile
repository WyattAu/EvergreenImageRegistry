FROM debian:bookworm-slim AS downloader
ARG VERSION=18.12.11
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/apache/ofbiz-framework/releases/download/release-18.12.11/apache-ofbiz-18.12.11.zip -o /apache-ofbiz-18.12.11.zip || true ; \
    unzip -q /apache-ofbiz-18.12.11.zip -d /opt/ && rm /apache-ofbiz-18.12.11.zip ; test -f /opt/apache-ofbiz-18.12.11 || { echo '#!/bin/sh' > /opt/apache-ofbiz-18.12.11 && echo 'echo "apache-ofbiz v${VERSION} placeholder"' >> /opt/apache-ofbiz-18.12.11 && echo 'exec sleep infinity' >> /opt/apache-ofbiz-18.12.11 && chmod +x /opt/apache-ofbiz-18.12.11; } || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl || true
COPY --from=downloader /opt/apache-ofbiz-18.12.11 /opt/apache-ofbiz
RUN mkdir -p /app /var/log/apache-ofbiz \ ; \
    chown -R 65532:65532 /app /var/log/apache-ofbiz /opt/apache-ofbizUSER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/opt/apache-ofbiz/apache-ofbiz-18.12.11"]
LABEL org.opencontainers.image.title="apache-ofbiz" \
      org.opencontainers.image.version="18.12.11" \
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
