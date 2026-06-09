ARG VERSION=6.9.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM taigaio/taiga-back:latest AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache ca-certificates curl python3 && \
    mkdir -p /var/log/taiga /taiga-back 2>/dev/null || true; \
    chown -R 65532:65532 /var/log/taiga /taiga-back 2>/dev/null || true

COPY --from=upstream /usr/local/bin/python3 /usr/local/bin/python3
COPY --from=upstream /usr/lib/python3 /usr/lib/python3
COPY --from=upstream /taiga-back /taiga-back

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true" \
    TAIGA_BACKEND_HOST="0.0.0.0"
WORKDIR /taiga-back
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8000"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/python3", "-m", "gunicorn", "taiga.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
LABEL org.opencontainers.image.title="taiga-back" \
      org.opencontainers.image.description="Taiga Backend - project management web application backend" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-back" \
      evergreen.image.tier="standard" \
      evergreen.image.category="project-management" \
      evergreen.image.status="functional" \
      evergreen.image.note="Repacked from taigaio/taiga-back upstream image" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
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
