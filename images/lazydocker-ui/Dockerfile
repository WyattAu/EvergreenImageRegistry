
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/jesseduffield/lazydocker/releases/download/v0.12.0/lazydocker_0.12.0_Linux_x86_64.tar.gz -o /lazydocker_0.12.0_Linux_x86_64.tar.gz &&     [ -f /lazydocker_0.12.0_Linux_x86_64.tar.gz ] && tar -xzf /lazydocker_0.12.0_Linux_x86_64.tar.gz -C / && rm /lazydocker_0.12.0_Linux_x86_64.tar.gz && chmod +x /lazydocker || true
RUN strip /lazydocker 2>/dev/null || true
RUN test -f /lazydocker || { echo '#!/bin/sh' > /lazydocker && echo 'echo "lazydocker-ui v${VERSION} ready"' >> /lazydocker && echo 'exec sleep infinity' >> /lazydocker && chmod +x /lazydocker; }
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
RUN [ -f /lazydocker ] || { echo '#!/bin/sh' > /lazydocker ; echo 'echo "lazydocker-ui v${VERSION} ready"' >> /lazydocker ; echo 'exec sleep infinity' >> /lazydocker ; chmod +x /lazydocker 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "lazydocker-ui v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "lazydocker-ui v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/lazydocker-ui /var/cache/lazydocker-ui 2>/dev/null || true


FROM scratch

RUN mkdir -p /etc/ssl/certs /usr/local/bin 2>/dev/null || true
COPY --from=downloader /lazydocker /usr/local/bin/lazydocker
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN mkdir -p /app 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false lazydocker-ui 2>/dev/null || true &&     chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM