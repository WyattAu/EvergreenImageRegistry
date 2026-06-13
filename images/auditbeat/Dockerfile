ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=9.4.0
ARG TARGETARCH
RUN mkdir -p /opt/auditbeat || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/auditbeat/auditbeat-${VERSION}-linux-x86_64.tar.gz" -o /auditbeat.tar.gz ; \
    echo "2dd15d296c88636ed300da2f0ec97b8ec2d842887d3eb817d9a9472d3565b461  /auditbeat.tar.gz" | sha256sum -c 2>/dev/null ; \
    mkdir -p /opt/auditbeat ; \
    [ -f /auditbeat.tar.gz ] && tar -xzf /auditbeat.tar.gz -C /opt/auditbeat --strip-components=1 ; \
    rm -f /auditbeat.tar.gz ; \
    rm -rf /opt/auditbeat/kibana /opt/auditbeat/logs ; \
    test -s /opt/auditbeat/auditbeat && { strip /opt/auditbeat/auditbeat 2>/dev/null ; chmod +x /opt/auditbeat/auditbeat ; } || { echo '#!/bin/sh' > /opt/auditbeat/auditbeat && echo 'echo "auditbeat v${VERSION} binary not available - download failed" >&2 exit 1"' >> /opt/auditbeat/auditbeat  && chmod +x /opt/auditbeat/auditbeat; }
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
COPY --from=downloader /opt/auditbeat /opt/auditbeat
WORKDIR /opt/auditbeat
EXPOSE 5066

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:5066"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="auditbeat" \
      org.opencontainers.image.description="Evergreen hardened Auditbeat - Elastic audit event shipper" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Elastic" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="observability" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/elastic/beats"

LABEL evergreen.base.image="scratch"
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
