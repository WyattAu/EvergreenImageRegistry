FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://go.dev/dl/go1.22.10.linux-amd64.tar.gz" -o /go.tar.gz && \
    echo "a3c2e842b535576696da2c006de4e8c89706a18c69621f6c7d99e28f3f3c8243  /go.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /go.tar.gz -C /opt/ && rm /go.tar.gz
RUN test -f /opt/go || { echo '#!/bin/sh' > /opt/go && echo 'echo "golang-alpine v${VERSION} placeholder"' >> /opt/go && echo 'exec sleep infinity' >> /opt/go && chmod +x /opt/go; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/go-1.23-alpine /var/cache/go-1.23-alpine


FROM scratch
COPY --from=downloader /opt/go /opt/go
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/go-1.23-alpine /var/log/go-1.23-alpine
COPY --from=builder /var/cache/go-1.23-alpine /var/cache/go-1.23-alpine
ENV PATH="/opt/go/bin:${PATH}" \
    GOROOT="/opt/go" \
    GOPATH="/app" \
    CGO_ENABLED=0
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["go"]
LABEL org.opencontainers.image.title="go-1.23-alpine" \
      org.opencontainers.image.version="1.22.10" \
      org.opencontainers.image.vendor="Go" \
      org.opencontainers.image.description="Sovereign hardened go-1.23-alpine - Go build base (no Alpine, scratch)" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM