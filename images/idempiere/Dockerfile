ARG VERSION=12.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/idempiere/idempiere/releases/download/release-12.4/idempiere-server-12.4.gtk.linux.x86_64.tar.gz" -o /idempiere-server-12.4.gtk.linux.x86_64.tar.gz && \
    unzip -q /idempiere-server-12.4.gtk.linux.x86_64.tar.gz -d /opt/ && rm /idempiere-server-12.4.gtk.linux.x86_64.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl
COPY --from=downloader /opt/idempiere-server-12.4.gtk.linux.x86_64 /opt/idempiere
RUN mkdir -p /app /var/log/idempiere \
    && chown -R 65532:65532 /app /var/log/idempiere /opt/idempiere
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/opt/idempiere/idempiere"]
LABEL org.opencontainers.image.title="idempiere" \
      org.opencontainers.image.version="12.4" \
      org.opencontainers.image.vendor="iDempiere" \
      org.opencontainers.image.source="https://github.com/idempiere/idempiere" \
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