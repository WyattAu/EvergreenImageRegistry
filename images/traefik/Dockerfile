ARG TARGETPLATFORM
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM debian:bookworm-slim AS downloader
ARG VERSION=v3.7.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/traefik/traefik/releases/download/${VERSION}/traefik_${VERSION}_linux_$(echo $TARGETPLATFORM | sed "s|linux/||").tar.gz" -o /traefik.tar.gz && \
    tar -xzf /traefik.tar.gz -C /tmp && \
    cp /tmp/traefik /traefik && \
    chmod +x /traefik

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim
COPY --from=downloader /traefik /traefik
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER ${APP_UID}:${APP_GID}
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /
EXPOSE 80 443 8080 9101
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]
ENTRYPOINT ["/shim", "run", "-c", "/traefik"]
LABEL org.opencontainers.image.title="traefik" \
      org.opencontainers.image.description="Traefik - modern HTTP reverse proxy and load balancer" \
      org.opencontainers.image.version="v3.7.1" \
      org.opencontainers.image.vendor="Traefik Labs" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.source="https://github.com/traefik/traefik" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch" \
      evergreen.build.type="binary-download" \
      evergreen.metrics.native="ztunnel" \
      evergreen.health.type="http" \
      evergreen.health.endpoint="/livez" \
      evergreen.health.listen="0.0.0.0:9101" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
