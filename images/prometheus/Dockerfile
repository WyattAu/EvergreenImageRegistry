ARG VERSION=2.54.0
ARG SHIM_VERSION=v1.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    arch=$(case ${TARGETARCH} in amd64) echo "amd64";; arm64) echo "arm64";; *) echo "amd64";; esac) && \
    curl -fsSL "https://github.com/prometheus/prometheus/releases/download/v${VERSION}/prometheus-${VERSION}.linux-${arch}.tar.gz" -o /tmp/prom.tar.gz && \
    tar -xzf /tmp/prom.tar.gz -C /tmp && \
    cp /tmp/prometheus-${VERSION}.linux-${arch}/prometheus /prometheus && \
    cp /tmp/prometheus-${VERSION}.linux-${arch}/promtool /promtool && \
    chmod +x /prometheus /promtool

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /prometheus /prometheus
COPY --from=downloader /promtool /promtool
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

EXPOSE 9090 9101
VOLUME /prometheus
WORKDIR /prometheus

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9090"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/prometheus"]

LABEL org.opencontainers.image.title="prometheus" \
      org.opencontainers.image.description="Prometheus - Go binary, scratch, non-root" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distroless="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
