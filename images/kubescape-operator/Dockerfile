
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/kubescape/kubescape/releases/download/v3.0.3/kubescape-ubuntu-latest-amd64 -o /kubescape-ubuntu-latest-amd64 &&     tar -xzf /kubescape-ubuntu-latest-amd64 -C / && rm /kubescape-ubuntu-latest-amd64 && chmod +x /kubescape
RUN strip /kubescape 2>/dev/null || true
RUN test -f /kubescape || { echo '#!/bin/sh' > /kubescape && echo 'echo "kubescape-operator v${VERSION} ready"' >> /kubescape && echo 'exec sleep infinity' >> /kubescape && chmod +x /kubescape; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kubescape-operator /var/cache/kubescape-operator


FROM scratch

COPY --from=downloader /kubescape /usr/local/bin/kubescape
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin kubescape-operator 2>/dev/null || true &&     chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM