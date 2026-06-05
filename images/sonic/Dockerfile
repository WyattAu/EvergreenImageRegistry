ARG VERSION=v1.4.9
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM valeriansaliou/sonic:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/sonic /var/cache/sonic 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=upstream /usr/local/bin/sonic /sonic
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/sonic /var/log/sonic
COPY --from=builder /var/cache/sonic /var/cache/sonic

WORKDIR /app

EXPOSE 1491
EXPOSE 9101

LABEL org.opencontainers.image.title="sonic" org.opencontainers.image.version="1.4.0" org.opencontainers.image.vendor="valeriansaliou" org.opencontainers.image.source="https://github.com/valeriansaliou/sonic" org.opencontainers.image.description="Fast, lightweight search backend" evergreen.image.tier="1" evergreen.image.category="search" evergreen.image.status="best-effort" evergreen.image.note="Binary repacked from upstream image; ca-certificates copied" evergreen.constraint.nonroot="true" evergreen.constraint.base="scratch" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="5s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="scratch"
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
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:1491"]

ENTRYPOINT ["/shim", "run"]
