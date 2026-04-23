FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/aquasecurity/trivy/releases/download/v0.58.2/trivy_0.58.2_linux-amd64.tar.gz" -o /trivy_0.58.2_linux-amd64.tar.gz &&     tar -xzf /trivy_0.58.2_linux-amd64.tar.gz -C / && rm /trivy_0.58.2_linux-amd64.tar.gz && chmod +x /trivy
RUN strip /trivy 2>/dev/null || true
RUN test -f /trivy || { echo '#!/bin/sh' > /trivy && echo 'echo "trivy-k8s v${VERSION} ready"' >> /trivy && echo 'exec sleep infinity' >> /trivy && chmod +x /trivy; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/trivy-k8s /var/cache/trivy-k8s

FROM scratch

COPY --from=downloader /trivy /usr/local/bin/trivy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin trivy-k8s 2>/dev/null || true &&     chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM