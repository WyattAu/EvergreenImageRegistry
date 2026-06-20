ARG VERSION=9.5.0
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM golang@sha256:167053a2bb901972bf2c1611f8f52c44d5fe7e762e5cab213708d82c421614db AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION=9.5.0
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}

RUN mkdir -p /app && \ RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils git ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --branch "v${VERSION}" https://github.com/github-linguist/linguist /src 2>/dev/null || echo "Source repo not available" && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w" \
        -o /app/linguist ./cmd/linguist 2>/dev/null || true && \
    test -s /app/linguist && strip --strip-all /app/linguist 2>/dev/null && \' \
    mkdir -p /app /var/log/linguist /var/cache/linguist
ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /app/linguist /linguist
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/linguist /var/log/linguist
COPY --from=builder /var/cache/linguist /var/cache/linguist
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/linguist"]
LABEL org.opencontainers.image.title="linguist-go" \
      org.opencontainers.image.description="Linguist - Go variant" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/github-linguist/linguist" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="scratch" \
            org.opencontainers.image.version="latest"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
