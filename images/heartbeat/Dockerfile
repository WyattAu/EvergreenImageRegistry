ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=9.4.0
ARG TARGETARCH
RUN mkdir -p /opt/heartbeat || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-${VERSION}-linux-x86_64.tar.gz" -o /heartbeat.tar.gz ; \
    echo "711083ec654168da15f3e4e8b924be00bf82b44c7427896ee59fe29431fe13ed  /heartbeat.tar.gz" | sha256sum -c ; \
    mkdir -p /opt/heartbeat ; \
    if [ -f /heartbeat.tar.gz ]; then tar -xzf /heartbeat.tar.gz -C /opt/heartbeat --strip-components=1 && rm -f /heartbeat.tar.gz && rm -rf /opt/heartbeat/kibana /opt/heartbeat/logs ; fi ; \
    strip /opt/heartbeat/heartbeat 2>/dev/null ; \
    chmod +x /opt/heartbeat/heartbeat 2>/dev/null ; && { echo "Binary not available - download failed" >&2; exit 1; }


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/log/heartbeat /var/lib/heartbeat /var/cache/heartbeat


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /opt/heartbeat /opt/heartbeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/heartbeat /var/log/heartbeat
COPY --from=builder /var/lib/heartbeat /var/lib/heartbeat
COPY --from=builder /var/cache/heartbeat /var/cache/heartbeat
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/heartbeat
EXPOSE 5066

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:5066"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="heartbeat" \
      org.opencontainers.image.description="Evergreen hardened Heartbeat - Elastic uptime monitor" \
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
