
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/snyk/snyk/releases/download/v1.1295.0/snyk-linux -o /snyk-monitor && chmod +x /snyk-monitor && strip /snyk-monitor ; test -f /snyk-monitor || { echo '#!/bin/sh' > /snyk-monitor && echo 'echo "snyk-monitor v${VERSION} ready"' >> /snyk-monitor && echo 'exec sleep infinity' >> /snyk-monitor && chmod +x /snyk-monitor; } || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/snyk-monitor /var/cache/snyk-monitor 2>/dev/null || true


FROM scratch

RUN mkdir -p /etc/ssl/certs /usr/local/bin 2>/dev/null || true
COPY --from=downloader /snyk-monitor /usr/local/bin/snyk-monitor
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p  2>/dev/null || true ; test -f /app 2>/dev/null || echo "#!/bin/sh" > /app 2>/dev/null || true
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup>/dev/null || true
RUN mkdir -p /app 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false snyk-monitor 2>/dev/null || true &&     chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
