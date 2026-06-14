
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.20.15
RUN mkdir -p /opt/paperless-ngx || true
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv python3-pip curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    python3 -m venv /opt/paperless-ngx && \
    /opt/paperless-ngx/bin/pip install --no-cache-dir paperless-ngx[all]==2.20.14

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /shim

LABEL evergreen.base.fallback_reason="wolfi-base for musl compatibility"
ARG VERSION=2.20.15

RUN apk add --no-cache ca-certificates tzdata python3 py3-pip curl libstdc++ zlib libjpeg-turbo tesseract poppler && \
    mkdir -p /opt/paperless-ngx /usr/src/paperless /var/lib/paperless /var/log/paperless /etc/paperless 2>/dev/null || true
COPY --from=downloader /opt/paperless-ngx /opt/paperless-ngx
RUN ln -sf /opt/paperless-ngx/bin/paperless /usr/local/bin/paperless 2>/dev/null || true && \
    chown -R 65532:65532 /opt/paperless-ngx /var/lib/paperless /var/log/paperless /etc/paperless 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /usr/src/paperless
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8000"]

ENTRYPOINT ["/shim", "run", "-c", "s6-svscan /etc/s6"]
LABEL org.opencontainers.image.title="paperless-ngx" \
      org.opencontainers.image.description="Paperless-ngx - document management system" \
      org.opencontainers.image.version="2.20.15" \
      org.opencontainers.image.vendor="Paperless-ngx" \
      org.opencontainers.image.source="https://github.com/paperless-ngx/paperless-ngx" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="document-management" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
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
