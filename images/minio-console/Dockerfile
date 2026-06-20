ARG VERSION=RELEASE.2025-09-07T16-13-09Z
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532



ARG SHIM_VERSION=v1.2.0

FROM minio/minio:RELEASE.2025-09-07T16-13-09Z@sha256:9966a92a734f9411e32f4f41d7d9d826fcdc0f68c4e20b70295bd4e7c11f8a2f AS upstream



FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim


COPY --from=upstream /usr/bin/minio /minio

COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

WORKDIR /app

EXPOSE 9000 9090




HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9000"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/minio"]

CMD ["--", "console", "server"]

LABEL org.opencontainers.image.title="minio-console"       org.opencontainers.image.version="RELEASE.2025-09-07T16-13-09Z"       org.opencontainers.image.vendor="MinIO"       org.opencontainers.image.source="https://github.com/minio/minio"       evergreen.image.tier="2"       evergreen.image.category="cloud-storage"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="scratch"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="5s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="10000ms" \
org.opencontainers.image.description="MinIO Console - web-based administration UI for MinIO" \
evergreen.base.image="scratch"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
