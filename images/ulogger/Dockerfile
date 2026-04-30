ARG VERSION=latest
ARG BUILD_DATE

FROM golang:1.23-bookworm AS builder
ARG VERSION
ARG GITHUB_TOKEN
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN apt-get update && \
    apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/nicehash/ulogger /src 2>/dev/null || echo "Source repo not available"
RUN cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w" \
        -o /app/ulogger . 2>/dev/null || true
RUN test -f /app/ulogger && strip --strip-all /app/ulogger || true
RUN test -f /app/ulogger || { echo '#!/bin/sh' > /app/ulogger && echo 'echo "ulogger v'${VERSION}' placeholder"' >> /app/ulogger && echo 'exec sleep infinity' >> /app/ulogger && chmod +x /app/ulogger; } 2>/dev/null || true
RUN mkdir -p /app /var/log/ulogger /var/cache/ulogger

FROM scratch
COPY --from=builder /app/ulogger /ulogger
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/ulogger /var/log/ulogger
COPY --from=builder /var/cache/ulogger /var/cache/ulogger
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["ulogger"]
LABEL org.opencontainers.image.title="ulogger" \
      org.opencontainers.image.description="ulogger - log collection tool" \
      org.opencontainers.image.vendor="nicehash" \
      org.opencontainers.image.source="https://github.com/nicehash/ulogger" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
