ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.5.2
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/Graylog2/collector-sidecar/releases/download/1.5.2/graylog-sidecar-1.5.2.tar.gz -o /sidecar.tar.gz 2>/dev/null ; \
    echo "bb8ea480268551864d246e31b3e5cc50e941e71b7ad236092a9b2ccb96b5eb0f  /sidecar.tar.gz" | sha256sum -c ; \
    mkdir -p /opt/sidecar-src /opt/sidecar || true ; \
    [ -f /sidecar.tar.gz ] && tar -xzf /sidecar.tar.gz -C /opt/sidecar-src --strip-components=1 2>/dev/null ; \
    rm -f /sidecar.tar.gz ; && { echo "Binary not available - download failed" >&2; exit 1; }
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/log/sidecar /var/lib/sidecar /var/cache/sidecar 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /opt/sidecar /opt/sidecar
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/sidecar /var/log/sidecar
COPY --from=builder /var/lib/sidecar /var/lib/sidecar
COPY --from=builder /var/cache/sidecar /var/cache/sidecar
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/sidecar
EXPOSE 8989

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8989"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="graylog-sidecar" \
      org.opencontainers.image.description="Evergreen hardened Graylog Sidecar - log collector management agent" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Graylog" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="observability" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/Graylog2/collector-sidecar"

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
