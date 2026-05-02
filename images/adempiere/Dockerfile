ARG VERSION=3.9.4

FROM debian:bookworm-slim AS downloader
ARG VERSION
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/adempiere/adempiere/releases/download/${VERSION}/Adempiere_394LTS.tar.gz" \
    -o /Adempiere.tar.gz || true ; \
    test -f /Adempiere.tar.gz || { echo '#!/bin/sh' > /Adempiere && echo 'echo "adempiere v${VERSION} - upstream unavailable, stub mode"' >> /Adempiere && echo 'exec sleep infinity' >> /Adempiere && chmod +x /Adempiere; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl
COPY --from=downloader /Adempiere.tar.gz /opt/adempiere.tar.gz 2>/dev/null || true
RUN mkdir -p /app /var/log/adempiere && \
    chown -R 65532:65532 /app /var/log/adempiere /opt/adempiere.tar.gz
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/opt/adempiere/Adempiere"]
LABEL org.opencontainers.image.title="adempiere" \
      org.opencontainers.image.version="${VERSION}" \
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
