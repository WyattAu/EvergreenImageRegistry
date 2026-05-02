ARG VERSION=0.25.0

FROM scratch
COPY --from=downloader /windows_exporter /windows_exporter 2>/dev/null || true
USER 65532:65532
WORKDIR /tmp
EXPOSE 9182
ENTRYPOINT ["/bin/sh", "-c", "echo 'windows-exporter v${VERSION} is Windows-only. Use prometheus-node-exporter for Linux metrics.'; sleep infinity"]
LABEL org.opencontainers.image.title="windows-exporter" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="prometheus-community" \
      org.opencontainers.image.source="https://github.com/prometheus-community/windows_exporter" \
      org.opencontainers.image.description="Prometheus exporter for Windows metrics (Windows-only, stub on Linux)" \
      sovereign.image.tier="1" \
      sovereign.image.category="monitoring" \
      sovereign.image.status="functional" \
      sovereign.image.note="This is a stub - windows-exporter only runs on Windows. Use prometheus-node-exporter for Linux." \
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
