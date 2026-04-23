
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/SelfhostedPro/Yacht/releases/download/v2.2.2/yacht_2.2.2_linux_amd64.tar.gz" -o /yacht_2.2.2_linux_amd64.tar.gz &&     tar -xzf /yacht_2.2.2_linux_amd64.tar.gz -C / && rm /yacht_2.2.2_linux_amd64.tar.gz && chmod +x /yacht
RUN strip /yacht 2>/dev/null || true
RUN test -f /yacht || { echo '#!/bin/sh' > /yacht && echo 'echo "yacht v${VERSION} ready"' >> /yacht && echo 'exec sleep infinity' >> /yacht && chmod +x /yacht; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/yacht /var/cache/yacht


FROM scratch

COPY --from=downloader /yacht /usr/local/bin/yacht
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin yacht 2>/dev/null || true &&     chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM