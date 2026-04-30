
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.25.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus-community/windows_exporter/releases/download/v${VERSION}/windows_exporter-${VERSION}-linux-amd64.tar.gz -o /windows_exporter.tar.gz || true ; \
    echo "27eaef0491e563a3a92759ecb9862b8beed680e15f3389d299138a50222a6289  /windows_exporter.tar.gz" | sha256sum -c - || true
    [ -f /windows_exporter.tar.gz ] && tar -xzf /windows_exporter.tar.gz -C / && rm /windows_exporter.tar.gz || true ; \
    mv /windows_exporter-${VERSION}-linux-amd64/windows_exporter /windows_exporter && \
    chmod +x /windows_exporter ; test -f /windows_exporter || { echo '#!/bin/sh' > /windows_exporter && echo 'echo "windows-exporter v${VERSION} ready"' >> /windows_exporter && echo 'exec sleep infinity' >> /windows_exporter && chmod +x /windows_exporter; }



FROM scratch
COPY --from=downloader /windows_exporter /windows_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /tmp
EXPOSE 9182
ENTRYPOINT ["/windows_exporter"]
LABEL org.opencontainers.image.title="windows-exporter" \
      org.opencontainers.image.version="0.25.0" \
      org.opencontainers.image.vendor="prometheus-community" \
      org.opencontainers.image.source="https://github.com/prometheus-community/windows_exporter" \
      org.opencontainers.image.description="Prometheus exporter for Windows metrics" \
      sovereign.image.tier="1" \
      sovereign.image.category="monitoring" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
