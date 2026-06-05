ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM golang:1.24-bookworm@sha256:98d673f18a1aac43da744209873cb79323e11706f909251bcfb131828b95559d AS builder
ARG VERSION=2.45.1
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
ENV GOTOOLCHAIN=auto
RUN mkdir -p /app && \
    apt-get update && \
    apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --depth 1 --branch "v${VERSION}" https://github.com/dexidp/dex /src && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build -ldflags="-s -w" -o /dex ./cmd/dex && \
    strip /dex

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=builder /dex /dex
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 5556

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:5556"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="dex" \
      org.opencontainers.image.description="Dex - federated OpenID Connect provider" \
      org.opencontainers.image.version="2.45.1" \
      org.opencontainers.image.vendor="DexIDP" \
      org.opencontainers.image.source="https://github.com/dexidp/dex" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      org.opencontainers.image.source="https://github.com/dexidp/dex"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
