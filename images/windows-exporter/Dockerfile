# STUB: windows-exporter is Windows-only, no Linux binary exists.
# This image is a no-op on Linux; it exists for registry completeness.
ARG VERSION=0.25.0

FROM scratch
USER 65532:65532
WORKDIR /tmp
EXPOSE 9182

HEALTHCHECK NONE
ENTRYPOINT ["/bin/sh", "-c", "echo 'windows-exporter v${VERSION} is Windows-only. Use prometheus-node-exporter for Linux metrics.'; sleep infinity"]
LABEL org.opencontainers.image.title="windows-exporter" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="prometheus-community" \
      org.opencontainers.image.source="https://github.com/prometheus-community/windows_exporter" \
      org.opencontainers.image.description="Prometheus exporter for Windows metrics (Windows-only, stub on Linux)" \
      evergreen.image.tier="1" \
      evergreen.image.category="monitoring" \
      evergreen.image.status="functional" \
      evergreen.image.note="This is a stub - windows-exporter only runs on Windows. Use prometheus-node-exporter for Linux." \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
