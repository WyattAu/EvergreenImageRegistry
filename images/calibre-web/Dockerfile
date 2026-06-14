ARG VERSION=0.6.26
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

# Calibre-web is a Python Flask app — needs python3 runtime
# Use upstream linuxserver image as source since no standalone binary exists
FROM lscr.io/linuxserver/calibre-web:${VERSION} AS calibre-upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache python3 ca-certificates

COPY --from=calibre-upstream /app/ /app/
COPY --from=calibre-upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8083

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8083"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "python3 /app/calibre-web.py"]
LABEL org.opencontainers.image.title="calibre-web" \
      org.opencontainers.image.description="calibre-web container image" \
      org.opencontainers.image.version="0.6.26" \
      org.opencontainers.image.vendor="Calibre-Web" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
      org.opencontainers.image.source="https://github.com/janeczku/calibre-web"
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
