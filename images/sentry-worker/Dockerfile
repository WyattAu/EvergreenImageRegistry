ARG VERSION=nightly
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM getsentry/sentry:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=nightly
RUN apk add --no-cache ca-certificates libpq libxml2 libxslt libffi openssl git
COPY --from=upstream /usr/src/sentry /opt/sentry
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/sentry 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9000"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "sentry", "--", "worker"]
LABEL org.opencontainers.image.title="sentry-worker"       org.opencontainers.image.version="26.4.1"       org.opencontainers.image.vendor="Sentry"       org.opencontainers.image.source="https://github.com/getsentry/self-hosted"       evergreen.image.tier="2"       evergreen.image.category="monitoring"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="wolfi"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="30s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="60000ms" \
      org.opencontainers.image.description="sentry-worker container image" \
evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
