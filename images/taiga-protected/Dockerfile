ARG VERSION=6.9.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=6.9.0
RUN mkdir -p /venv || true
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-venv curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir taiga-protected==${VERSION} 2>/dev/null && \
    mkdir -p /app /var/log/taiga-protected /etc/taiga-protected 2>/dev/null || true

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /shim

LABEL evergreen.base.fallback_reason="wolfi-base for musl compatibility"
RUN apk add --no-cache python3 ca-certificates libstdc++ 2>/dev/null || true
COPY --from=downloader /venv /venv
COPY --from=downloader /var/log/taiga-protected /var/log/taiga-protected
COPY --from=downloader /etc/taiga-protected /etc/taiga-protected
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8003

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8003"]

ENTRYPOINT ["/shim", "run", "-c", "nginx -g "daemon off;""]

LABEL org.opencontainers.image.title="taiga-protected" \
      org.opencontainers.image.description="Taiga Protected - file access protection proxy for Taiga" \
      org.opencontainers.image.version="6.9.0" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-protected" \
      evergreen.image.tier="3" \
      evergreen.image.category="project-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"

LABEL evergreen.base.image="wolfi"
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
