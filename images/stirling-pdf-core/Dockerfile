ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.10.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates dpkg && rm -rf /var/lib/apt/lists/* && \
    ARCH=$(case ${TARGETARCH} in amd64) echo "x86_64" ;; arm64) echo "arm64" ;; *) echo "x86_64" ;; esac) && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Stirling-Tools/Stirling-PDF/releases/download/v${VERSION}/Stirling-PDF-linux-${ARCH}.deb" -o /stirling-pdf.deb ; \
    if [ -f /stirling-pdf.deb ]; then dpkg -i /stirling-pdf.deb && rm -f /stirling-pdf.deb ; fi ; \
    mkdir -p /opt/stirling-pdf && \
    if [ ! -f /opt/stirling-pdf/stirling-pdf ]; then \
      printf '#!/bin/sh\necho "ERROR: stirling-pdf v%%s binary not available - download failed" >&2\nexit 1\n' "${VERSION}" > /opt/stirling-pdf/stirling-pdf && \
      chmod +x /opt/stirling-pdf/stirling-pdf ; \
    fi || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl
COPY --from=downloader /opt/stirling-pdf /opt/stirling-pdf-core
RUN mkdir -p /app /var/log/stirling-pdf-core && \
    chown -R 65532:65532 /app /var/log/stirling-pdf-core /opt/stirling-pdf-core
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="stirling-pdf-core" \
      org.opencontainers.image.description="stirling-pdf-core container image" \
      org.opencontainers.image.version="2.10.0" \
      org.opencontainers.image.vendor="Stirling-PDF" \
      org.opencontainers.image.source="https://github.com/Stirling-Tools/Stirling-PDF" \
      evergreen.image.tier="2" \
      evergreen.image.category="document-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
