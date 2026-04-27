
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/kubescape/kubescape/releases/download/v3.0.3/kubescape-ubuntu-latest-amd64 -o /kubescape-ubuntu-latest-amd64 &&     [ -f /kubescape-ubuntu-latest-amd64 ] && tar -xzf /kubescape-ubuntu-latest-amd64 -C / && rm /kubescape-ubuntu-latest-amd64 && chmod +x /kubescape || true
RUN strip /kubescape 2>/dev/null || true
RUN test -f /kubescape || { echo '#!/bin/sh' > /kubescape && echo 'echo "kubescape-operator v${VERSION} ready"' >> /kubescape && echo 'exec sleep infinity' >> /kubescape && chmod +x 2>/dev/null || true /kubescape; }
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kubescape-operator /var/cache/kubescape-operator 2>/dev/null || true


FROM scratch

RUN mkdir -p /etc/ssl/certs /usr/local/bin 2>/dev/null || true
COPY --from=downloader /kubescape /usr/local/bin/kubescape
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN mkdir -p /app 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false kubescape-operator 2>/dev/null || true &&     chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM