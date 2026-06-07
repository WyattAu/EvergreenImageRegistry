ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader

ARG VERSION=260305-fad9d5395

ARG TARGETARCH

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/photoprism/photoprism/releases/download/${VERSION}/photoprism_${VERSION}-linux-${TARGETARCH}.tar.gz" \
    -o /tmp/photoprism.tar.gz 2>/dev/null && \
    mkdir -p /tmp/photoprism-extract && \
    tar -xzf /tmp/photoprism.tar.gz -C /tmp/photoprism-extract 2>/dev/null && \
    cp /tmp/photoprism-extract/photoprism /photoprism 2>/dev/null || find /tmp/photoprism-extract -name 'photoprism' -type f -exec cp {} /photoprism \; 2>/dev/null && \
    chmod +x /photoprism 2>/dev/null && \
    rm -rf /tmp/photoprism.tar.gz /tmp/photoprism-extract 2>/dev/null

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim


COPY --from=downloader /photoprism /photoprism

COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

WORKDIR /app

EXPOSE 2282




HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:2282"]

ENTRYPOINT ["/shim", "run"]

LABEL org.opencontainers.image.title="photoprism-bin"       org.opencontainers.image.version="260305-fad9d5395"       org.opencontainers.image.vendor="PhotoPrism"       org.opencontainers.image.source="https://github.com/photoprism/photoprism"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms" \
org.opencontainers.image.description="photoprism-bin container image" \
evergreen.base.image="scratch"

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
