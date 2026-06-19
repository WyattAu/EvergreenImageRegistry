ARG TARGETARCH
ARG SHIM_VERSION=v1.2.0

FROM golang:1.22-alpine AS builder
ARG VERSION=2.0.0
RUN apk add --no-cache git ca-certificates
ENV GO111MODULE=off
ENV GOPATH=/go
RUN go get -d github.com/michenriksen/gitrob/... && \
    cd /go/src/github.com/michenriksen/gitrob && \
    CGO_ENABLED=0 go build -ldflags="-s -w" -o /gitrob ./cmd/gitrob || \
    CGO_ENABLED=0 go build -ldflags="-s -w" -o /gitrob .

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /gitrob /gitrob
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9101"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/gitrob"]
LABEL org.opencontainers.image.title="gitrob" \
      org.opencontainers.image.description="GitRob - sensitive file finder for GitHub repositories" \
      org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.vendor="michenriksen" \
      org.opencontainers.image.source="https://github.com/michenriksen/gitrob" \
      evergreen.image.tier="standard" \
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
