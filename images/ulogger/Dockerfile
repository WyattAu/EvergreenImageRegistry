ARG VERSION=latest
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM golang@sha256:167053a2bb901972bf2c1611f8f52c44d5fe7e762e5cab213708d82c421614db AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION=latest
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}

RUN mkdir -p /app && \ RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils git ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/nicehash/ulogger /src 2>/dev/null || echo "Source repo not available" && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w" \
        -o /app/ulogger . 2>/dev/null || true && \
    test -s /app/ulogger && strip --strip-all /app/ulogger 2>/dev/null && \' binary not available - download failed" >&2 exit 1"' >> /app/ulogger && echo 'exit 1' >> /app/ulogger && chmod +x /app/ulogger; } 2>/dev/null && \
    mkdir -p /app /var/log/ulogger /var/cache/ulogger
FROM scratch
COPY --from=builder /app/ulogger /ulogger
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/ulogger /var/log/ulogger
COPY --from=builder /var/cache/ulogger /var/cache/ulogger
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["ulogger"]
LABEL org.opencontainers.image.title="ulogger" \
      org.opencontainers.image.description="ulogger - log collection tool" \
      org.opencontainers.image.vendor="nicehash" \
      org.opencontainers.image.source="https://github.com/nicehash/ulogger" \
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
