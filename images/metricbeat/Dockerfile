ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=9.4.0
ARG TARGETARCH
RUN mkdir -p /opt/metricbeat || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-${VERSION}-linux-x86_64.tar.gz" -o /metricbeat.tar.gz ; \
    echo "ced529e586ee32a9622e963097fbfcdb79615da6f4e02b8200029fd1f11b9d76  /metricbeat.tar.gz" | sha256sum -c ; \
    mkdir -p /opt/metricbeat ; \
    if [ -f /metricbeat.tar.gz ]; then tar -xzf /metricbeat.tar.gz -C /opt/metricbeat --strip-components=1 && rm -f /metricbeat.tar.gz && rm -rf /opt/metricbeat/kibana /opt/metricbeat/logs ; fi ; \
    strip /opt/metricbeat/metricbeat 2>/dev/null ; \
    chmod +x /opt/metricbeat/metricbeat 2>/dev/null


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/log/metricbeat /var/lib/metricbeat /var/cache/metricbeat


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /opt/metricbeat /opt/metricbeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/metricbeat /var/log/metricbeat
COPY --from=builder /var/lib/metricbeat /var/lib/metricbeat
COPY --from=builder /var/cache/metricbeat /var/cache/metricbeat
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/metricbeat
EXPOSE 5066

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:5066"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="metricbeat" \
      org.opencontainers.image.description="Evergreen hardened Metricbeat - Elastic infrastructure metrics collector" \
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
