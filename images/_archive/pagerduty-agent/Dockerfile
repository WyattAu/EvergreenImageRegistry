ARG TARGETARCH
ARG SHIM_VERSION=v1.2.0

FROM golang:1.22-alpine AS builder
ARG VERSION=1.7.4
RUN apk add --no-cache git ca-certificates
RUN git clone --depth 1 https://github.com/PagerDuty/pdagent.git /src && \
    cd /src && \
    CGO_ENABLED=0 go build -ldflags="-s -w" -o /pdagent . 2>/dev/null || \
    (go mod init pdagent && CGO_ENABLED=0 go build -ldflags="-s -w" -o /pdagent .)

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /pdagent /pdagent
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9101"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/pdagent"]
LABEL org.opencontainers.image.title="pagerduty-agent" \
      org.opencontainers.image.description="PagerDuty pdagent - event orchestration agent" \
      org.opencontainers.image.version="1.7.4" \
      org.opencontainers.image.vendor="PagerDuty" \
      org.opencontainers.image.source="https://github.com/PagerDuty/pdagent" \
      evergreen.image.tier="standard" \
      evergreen.image.category="monitoring" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
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
