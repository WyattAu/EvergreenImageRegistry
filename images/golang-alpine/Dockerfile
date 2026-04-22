ARG VERSION=1.22.10
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://go.dev/dl/go1.22.10.linux-amd64.tar.gz" -o /go.tar.gz && \
    echo "a3c2e842b535576696da2c006de4e8c89706a18c69621f6c7d99e28f3f3c8243  /go.tar.gz" | sha256sum -c - && \
    tar -xzf /go.tar.gz -C /opt/ && rm /go.tar.gz

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/golang-alpine /var/cache/golang-alpine

FROM scratch
COPY --from=downloader /opt/go /opt/go
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/golang-alpine /var/log/golang-alpine
COPY --from=builder /var/cache/golang-alpine /var/cache/golang-alpine
ENV PATH="/opt/go/bin:${PATH}" \
    GOROOT="/opt/go" \
    GOPATH="/app" \
    CGO_ENABLED=0
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["go", "version"]
ENTRYPOINT ["go"]
LABEL org.opencontainers.image.title="golang-alpine" \
      org.opencontainers.image.version="1.22.10" \
      org.opencontainers.image.vendor="Go" \
      org.opencontainers.image.description="Sovereign hardened golang-alpine - Go build base (no Alpine, scratch)" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"
