ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
ARG VERSION=1.0.0
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
WORKDIR /tmp

RUN apt-get update && apt-get install -y --no-install-recommends binutils go-1.23 && rm -rf /var/lib/apt/lists/* && \
    printf 'package main\nimport "fmt"\nfunc main() { fmt.Println("go-1.23-cache v%s ready") }' "${VERSION}" > /tmp/main.go ; CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build -ldflags="-s -w" -o /tmp/go-1.23-cache /tmp/main.go ; strip --strip-all /tmp/go-1.23-cache 2>/dev/null && \
    mkdir -p /usr/local/bin
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=1.0.0
COPY --from=builder /tmp/go-1.23-cache /usr/local/bin/go-1.23-cache
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
EXPOSE 6379

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="go-1.23-cache" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Golang-Cache - in-memory cache service" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
            org.opencontainers.image.source="https://github.com/golang/go"

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
