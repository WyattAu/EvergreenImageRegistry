ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.5.0
ARG TARGETARCH
RUN mkdir -p /tmp/drone-autoscaler || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/harness/drone/releases/download/v${VERSION}/drone_autoscaler_linux_amd64.tar.gz" \
    -o /tmp/archive.tar.gz && \
    tar -xzf /tmp/archive.tar.gz -C /tmp && \
    strip /tmp/drone-autoscaler&& \
    chmod +x /tmp/drone-autoscaler
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /tmp/drone-autoscaler /usr/local/bin/drone-autoscaler
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="drone-autoscaler" \
      org.opencontainers.image.description="Drone Autoscaler - automatic scaling for Drone runners" \
      org.opencontainers.image.version="1.5.0" \
      org.opencontainers.image.vendor="Harness" \
      org.opencontainers.image.source="https://github.com/harness/drone" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
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
