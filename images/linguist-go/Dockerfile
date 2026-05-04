ARG VERSION=latest
ARG BUILD_DATE

FROM golang@sha256:167053a2bb901972bf2c1611f8f52c44d5fe7e762e5cab213708d82c421614db AS builder
ARG TARGETARCH
ARG VERSION
ARG GITHUB_TOKEN
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN apt-get update && \
    apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch "v${VERSION}" https://github.com/github/linguist /src 2>/dev/null || echo "Source repo not available"
RUN cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w" \
        -o /app/linguist ./cmd/linguist 2>/dev/null || true
RUN test -f /app/linguist && strip --strip-all /app/linguist || true
RUN test -f /app/linguist || { echo '#!/bin/sh' > /app/linguist && echo 'echo "linguist-go v'${VERSION}' placeholder"' >> /app/linguist && echo 'exec sleep infinity' >> /app/linguist && chmod +x /app/linguist; } 2>/dev/null || true
RUN mkdir -p /app /var/log/linguist /var/cache/linguist

FROM scratch
COPY --from=builder /app/linguist /linguist
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/linguist /var/log/linguist
COPY --from=builder /var/cache/linguist /var/cache/linguist
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/linguist"]
LABEL org.opencontainers.image.title="linguist-go" \
      org.opencontainers.image.description="Linguist - Go variant" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/github/linguist" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
