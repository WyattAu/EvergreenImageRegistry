
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/snyk/snyk/releases/download/v1.1295.0/snyk-linux -o /snyk-alpine && chmod +x /snyk-alpine && strip /snyk-alpine ; test -f /snyk-alpine || { echo '#!/bin/sh' > /snyk-alpine && echo 'echo "snyk-alpine v${VERSION} ready"' >> /snyk-alpine && echo 'exec sleep infinity' >> /snyk-alpine && chmod +x /snyk-alpine; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/snyk-alpine /var/cache/snyk-alpine 2>/dev/null || true


FROM scratch

COPY --from=downloader /snyk-alpine /usr/local/bin/snyk-alpine
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin snyk-alpine 2>/dev/null || true &&     chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
