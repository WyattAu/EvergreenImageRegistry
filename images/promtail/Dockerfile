ARG VERSION=3.6.11
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=3.6.11
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/grafana/loki/releases/download/v${VERSION}/promtail-linux-${TARGETARCH}.zip -o /promtail.zip ; \
    unzip -o /promtail.zip -d /tmp ; \
    strip --strip-all /tmp/promtail-linux-${TARGETARCH}/promtail 2>/dev/null; mv /tmp/promtail-linux-${TARGETARCH}/promtail /tmp/promtail 2>/dev/null ; \
    rm -f /promtail.zip 2>/dev/null || true

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim

ARG VERSION=3.6.11
COPY --from=downloader /tmp/promtail /usr/bin/promtail
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
EXPOSE 9080 3100

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9080"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/bin/promtail"]
LABEL org.opencontainers.image.title="promtail" \
      org.opencontainers.image.version="3.6.11" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Evergreen hardened Promtail - log collection agent for Grafana Loki" \
      evergreen.image.tier="1" \
      evergreen.image.category="logging" \
            org.opencontainers.image.source="https://github.com/grafana/loki"

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
