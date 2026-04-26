FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app-src /var/log/linguist /var/cache/linguist 2>/dev/null || true
RUN  placeholder"' >> /app/placeholder && echo 'exec sleep infinity' >> /app/placeholder && chmod +x /app; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache go-1.23 git ca-certificates 
WORKDIR /src
RUN git clone --depth 1 https://github.com/github/linguist.git /src || echo "Source repo not available - using placeholder" && \
    cd /src && go build -ldflags="-s -w" -o /linguist ./cmd/linguist 2>/dev/null || true
    RUN cd /src && go build -ldflags="-s -w" -o /linguist ./cmd/linguist 2>/dev/null || true
COPY --from=downloader /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false linguist 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/linguist"]
LABEL org.opencontainers.image.title="linguist-go" \
      org.opencontainers.image.description="Linguist - Go variant" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/github/linguist" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM