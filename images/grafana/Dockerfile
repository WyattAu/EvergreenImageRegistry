ARG TARGETARCH
ARG VERSION=12.2.8-security-04
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v0.3.0
FROM golang:1.26-bookworm AS builder
ARG TARGETARCH
ARG VERSION=12.2.8-security-04
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch "v${VERSION}" https://github.com/grafana/grafana.git . || \
    git clone --depth 1 https://github.com/grafana/grafana.git .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} \
    go build -ldflags='-s -w -X main.version=${VERSION}' \
    -o /grafana-server ./cmd/grafana-server
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim
FROM scratch
COPY --from=shim /shim /shim
COPY --from=builder /grafana-server /grafana-server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER ${APP_UID}:${APP_GID}
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /
EXPOSE 3000 9101
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]
ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="grafana" \
      org.opencontainers.image.description="Grafana - observability dashboard and visualization" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.source="https://github.com/grafana/grafana" \
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
