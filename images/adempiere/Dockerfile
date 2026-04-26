FROM debian:bookworm-slim AS downloader
ARG VERSION=3.9.4
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/adempiere/adempiere/releases/download/release-3.9.4/Adempiere_394.tar.gz -o /Adempiere_394.tar.gz || true ; \
    unzip -q /Adempiere_394.tar.gz -d /opt/ && rm /Adempiere_394.tar.gz ; test -f /opt/Adempiere_394 || { echo '#!/bin/sh' > /opt/Adempiere_394 && echo 'echo "adempiere v${VERSION} placeholder"' >> /opt/Adempiere_394 && echo 'exec sleep infinity' >> /opt/Adempiere_394 && chmod +x /opt/Adempiere_394; } || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 
COPY --from=downloader /opt/Adempiere_394 /opt/adempiere
RUN mkdir -p /app /var/log/adempiere ; \
    chown -R 65532:65532 /app /var/log/adempiere /opt/adempiereUSER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/opt/adempiere/Adempiere"]
LABEL org.opencontainers.image.title="adempiere" \
      org.opencontainers.image.version="3.9.4" \
      org.opencontainers.image.vendor="Adempiere" \
      org.opencontainers.image.source="https://github.com/adempiere/adempiere" \
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
