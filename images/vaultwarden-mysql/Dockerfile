ARG VERSION=1.35.8
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM vaultwarden/server@sha256:c4f6056fe0c288a052a223cecd263a90d1dda1a0177bb5b054a363a6c7b211d9 AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=1.35.8
RUN apk add --no-cache ca-certificates
COPY --from=upstream /vaultwarden /usr/local/bin/vaultwarden
RUN mkdir -p /app && chown 65532:65532 /app 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/vaultwarden", "--", "--database-url", "mysql://user:pass@host/db"]
LABEL org.opencontainers.image.title="vaultwarden-mysql"       org.opencontainers.image.version="1.35.8"       org.opencontainers.image.vendor="dani-garcia"       org.opencontainers.image.source="https://github.com/dani-garcia/vaultwarden"       evergreen.image.tier="2"       evergreen.image.category="secrets"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="wolfi"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms" \
      org.opencontainers.image.description="vaultwarden-mysql container image" \
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
