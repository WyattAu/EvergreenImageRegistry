ARG VERSION=nightly

FROM getsentry/sentry:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=nightly
RUN apk add --no-cache ca-certificates libpq libxml2 libxslt libffi openssl git
COPY --from=upstream /usr/src/sentry /opt/sentry
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/sentry 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9000/ || exit 1
ENTRYPOINT ["sentry"]
CMD ["worker"]
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
