ARG VERSION=5.0.5
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM fluent/fluent-bit:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=3.2.4
RUN apk add --no-cache wget ca-certificates
COPY --from=upstream /fluent-bit/bin/fluent-bit /usr/local/bin/fluent-bit
RUN mkdir -p /app /var/log/fluent-bit /var/cache/fluent-bit

WORKDIR /app

EXPOSE 2020
EXPOSE 9101

LABEL org.opencontainers.image.title="fluent-bit" org.opencontainers.image.version="5.0.5" org.opencontainers.image.vendor="Fluent" evergreen.image.tier="critical" evergreen.constraint.nonroot="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms" \
      org.opencontainers.image.source="https://github.com/fluent/fluent-bit" \
      org.opencontainers.image.description="Fluent Bit - fast lightweight log processor and forwarder" \
evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:2020"]

ENTRYPOINT ["/shim", "run", "-c", "fluent-bit"]
