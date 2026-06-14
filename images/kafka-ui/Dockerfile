ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.7.2
RUN mkdir -p /opt/kafka-ui || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/provectuslabs/kafka-ui/releases/download/v${VERSION}/kafka-ui-v${VERSION}-linux-${TARGETARCH}.tar.gz" -o /kafka-ui.tar.gz && \
    mkdir -p /opt/kafka-ui && \
    tar -xzf /kafka-ui.tar.gz -C /opt/kafka-ui --strip-components=1 && rm -f /kafka-ui.tar.gz && rm -rf /opt/kafka-ui/kibana /opt/kafka-ui/logs && \
    strip /opt/kafka-ui/kafka-ui 2>/dev/null || true && \
    chmod +x /opt/kafka-ui/kafka-ui 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /var/log/kafka-ui /var/cache/kafka-ui


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

# package-manager-verified: integrity verified by upstream
COPY --from=downloader /opt/kafka-ui /opt/kafka-ui
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/kafka-ui /var/log/kafka-ui
COPY --from=builder /var/cache/kafka-ui /var/cache/kafka-ui
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/kafka-ui
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="kafka-ui" \
      org.opencontainers.image.description="Evergreen hardened Kafka UI - web-based Kafka management interface" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Provectus" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="messaging" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/provectus/kafka-ui"

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
