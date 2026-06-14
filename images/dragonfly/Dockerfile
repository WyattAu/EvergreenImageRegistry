
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.18.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/dragonflydb/dragonfly/releases/download/v1.38.1/dragonfly-$(echo ${TARGETARCH} | sed 's/amd64/x86_64/;s/arm64/aarch64/').tar.gz -o /dragonfly.tar.gz ; \
    echo "26d69d1724d4905b193109d3dc8a18508e0aa235cec434d6d886a1feedbdab1e  /dragonfly.tar.gz" | sha256sum -c ; \
    [ -f /dragonfly.tar.gz ] && tar -xzf /dragonfly.tar.gz -C /tmp/ ; \
    chmod +x /tmp/dragonfly && \
    mv /tmp/dragonfly /dragonfly && \
    rm -rf /dragonfly.tar.gz /tmp/* && { echo "Binary not available - download failed" >&2; exit 1; }



FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /dragonfly /dragonfly
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 6379

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/shim", "run"]
CMD ["-c", "/dragonfly", "--", "--bind", "0.0.0.0:6379"]
LABEL org.opencontainers.image.title="dragonfly" \
      org.opencontainers.image.description="Dragonfly - in-memory data store compatible with Redis and Memcached" \
      org.opencontainers.image.version="1.18.0" \
      org.opencontainers.image.vendor="DragonflyDB" \
      org.opencontainers.image.source="https://github.com/dragonflydb/dragonfly" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
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
