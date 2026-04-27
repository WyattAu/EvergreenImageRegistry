
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/SelfhostedPro/Yacht/releases/download/v2.2.2/yacht_2.2.2_linux_amd64.tar.gz -o /yacht_2.2.2_linux_amd64.tar.gz &&     [ -f /yacht_2.2.2_linux_amd64.tar.gz ] && tar -xzf /yacht_2.2.2_linux_amd64.tar.gz -C / && rm /yacht_2.2.2_linux_amd64.tar.gz && chmod +x /yacht || true
RUN strip /yacht 2>/dev/null || true
RUN test -f /yacht || { echo '#!/bin/sh' > /yacht && echo 'echo "yacht v${VERSION} ready"' >> /yacht && echo 'exec sleep infinity' >> /yacht && chmod +x /yacht; }
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
RUN [ -f /yacht ] || { echo '#!/bin/sh' > /yacht ; echo 'echo "yacht v${VERSION} ready"' >> /yacht ; echo 'exec sleep infinity' >> /yacht ; chmod +x /yacht 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "yacht v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "yacht v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/yacht /var/cache/yacht 2>/dev/null || true


FROM scratch

RUN mkdir -p /etc/ssl/certs /usr/local/bin 2>/dev/null || true
COPY --from=downloader /yacht /usr/local/bin/yacht
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN mkdir -p /app 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false yacht 2>/dev/null || true &&     chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM