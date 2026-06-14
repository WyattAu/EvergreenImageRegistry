ARG VERSION=6.9.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM taigaio/taiga-events:latest AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache ca-certificates curl nodejs && \
    mkdir -p /var/log/taiga-events /taiga-events 2>/dev/null || true; \
    chown -R 65532:65532 /var/log/taiga-events /taiga-events 2>/dev/null || true

COPY --from=upstream /usr/local/bin/node /usr/local/bin/node
COPY --from=upstream /usr/lib/node_modules /usr/lib/node_modules
COPY --from=upstream /taiga-events /taiga-events

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true" \
    TAIGA_EVENTS_HOST="0.0.0.0"
WORKDIR /taiga-events
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8000"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/node", "index.js"]
LABEL org.opencontainers.image.title="taiga-events" \
      org.opencontainers.image.description="Taiga Events - real-time events service for Taiga" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-events" \
      evergreen.image.tier="standard" \
      evergreen.image.category="project-management" \
      evergreen.image.status="functional" \
      evergreen.image.note="Repacked from taigaio/taiga-events upstream image" \
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
