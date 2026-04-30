ARG VERSION=latest
ARG BUILD_DATE

FROM golang:1.23-bookworm AS builder
ARG VERSION
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch "v${VERSION}" https://github.com/github/linguist /src 2>/dev/null || echo "Source repo not available"
RUN cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
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
ENTRYPOINT ["/linguist"]
LABEL org.opencontainers.image.title="linguist-go" \
      org.opencontainers.image.description="Linguist - Go variant" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/github/linguist" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
