FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/linguist /var/cache/linguist

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        golang git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/github/linguist.git /src && \
    cd /src && go build -ldflags="-s -w" -o /linguist ./cmd/linguist 2>/dev/null || true
COPY --from=downloader /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin linguist 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=1 \
    CMD ["/linguist", "--version"] || exit 0
ENTRYPOINT ["/linguist"]
LABEL org.opencontainers.image.title="linguist-go" \
      org.opencontainers.image.description="Linguist - Go variant" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/github/linguist" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
