ARG VERSION=6.9.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* || true && \
    git clone --branch "v${VERSION}" https://github.com/taigaio/taiga-front-dist.git /tmp/taiga-front 2>/dev/null && \
    cd /tmp/taiga-front && npm install && npm run build 2>/dev/null && \
    mkdir -p /tmp/taiga-front/dist 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache git ca-certificates curl nginx
COPY --from=builder /tmp/taiga-front/dist /var/www/taiga-front
RUN mkdir -p /var/log/nginx /var/cache/nginx /var/www/taiga-front ; \
    chown -R 65532:65532 /var/www/taiga-front /var/log/nginx /var/cache/nginx
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /var/www/taiga-front
EXPOSE 80 443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/shim", "run", "-c", "nginx"]]
LABEL org.opencontainers.image.title="taiga-front" \
      org.opencontainers.image.description="taiga-front container image" \
      org.opencontainers.image.version="6.9.0" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-front-dist" \
      evergreen.image.tier="2" \
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
