FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/ulogger /var/cache/ulogger

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        golang git ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/nicehash/ulogger.git /src && \
    cd /src && go build -ldflags="-s -w" -o /ulogger .
RUN strip /ulogger 2>/dev/null || true

FROM scratch

COPY --from=builder /ulogger /usr/local/bin/ulogger
COPY --from=downloader /app /app
COPY --from=downloader /var/log/ulogger /var/log/ulogger
COPY --from=downloader /var/cache/ulogger /var/cache/ulogger
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin ulogger 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/ulogger /var/cache/ulogger 2>/dev/null || true
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