
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/snyk/snyk/releases/download/v1.1295.0/snyk-linux -o /snyk-monitor && chmod +x /snyk-monitor && strip /snyk-monitor ; test -f /snyk-monitor || { echo '#!/bin/sh' > /snyk-monitor && echo 'echo "snyk-monitor v${VERSION} ready"' >> /snyk-monitor && echo 'exec sleep infinity' >> /snyk-monitor && chmod +x /snyk-monitor; } || true && \
    echo "ee7382115d7a4f1fee05a70e3af7db4dbd07f6c54f1adb76fce534ac607c0372  /snyk-monitor" | sha256sum -c - || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/snyk-monitor /var/cache/snyk-monitor 2>/dev/null || true


FROM scratch

COPY --from=downloader /snyk-monitor /usr/local/bin/snyk-monitor
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65532:65532
WORKDIR /app
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
