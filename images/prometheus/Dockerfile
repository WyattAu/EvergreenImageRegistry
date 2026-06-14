ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.2.0
FROM golang:1.24-bookworm AS builder
ARG TARGETARCH
ARG VERSION=2.53.0
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch "v${VERSION}" https://github.com/prometheus/prometheus.git . || \
    git clone --depth 1 https://github.com/prometheus/prometheus.git .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} \
    go build -ldflags='-s -w -X main.version=${VERSION}' \
    -o /binary ./cmd/prometheus
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim
FROM scratch
COPY --from=shim /shim /shim
COPY --from=builder /binary /prometheus
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER ${APP_UID}:${APP_GID}
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /
EXPOSE 9090 9101
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9090"]
ENTRYPOINT ["/shim", "run", "-c", "prometheus"]
LABEL org.opencontainers.image.title="prometheus" \
      org.opencontainers.image.description="Prometheus - monitoring and alerting toolkit" \
      org.opencontainers.image.version="2.53.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.source="https://github.com/prometheus/prometheus" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch" \
      evergreen.build.type="musl-source" \
      evergreen.metrics.native="ztunnel" \
      evergreen.health.type="http" \
      evergreen.health.endpoint="/livez" \
      evergreen.health.listen="0.0.0.0:9101" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
