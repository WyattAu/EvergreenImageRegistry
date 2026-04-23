FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/snyk/snyk/releases/download/v1.1295.0/snyk-linux" -o /snyk-docker && chmod +x /snyk-docker && strip /snyk-docker

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/snyk-docker /var/cache/snyk-docker

FROM scratch

COPY --from=downloader /snyk-docker /usr/local/bin/snyk-docker
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin snyk-docker 2>/dev/null || true &&     chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM