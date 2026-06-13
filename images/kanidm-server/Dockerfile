ARG VERSION=1.9.4
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM docker.io/kanidm/server:1.9.4@sha256:7eecd3b5b179649abc2581d8d3119a9bb7602ef7f266c0b991593048f728e6e5 AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /var/log/kanidm-server /var/cache/kanidm-server 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=upstream /sbin/kanidmd /kanidmd
COPY --from=builder /app /app
COPY --from=builder /var/log/kanidm-server /var/log/kanidm-server
COPY --from=builder /var/cache/kanidm-server /var/cache/kanidm-server

WORKDIR /app

EXPOSE 8443
EXPOSE 9101

LABEL org.opencontainers.image.title="kanidm-server" org.opencontainers.image.version="1.9.4" org.opencontainers.image.vendor="Kanidm" org.opencontainers.image.source="https://github.com/kanidm/kanidm" evergreen.image.tier="2" evergreen.image.category="identity" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms" \
      org.opencontainers.image.description="kanidm-server container image" \
evergreen.base.image="scratch"
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
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8443"]

ENTRYPOINT ["/shim", "run", "-c", "kanidm"]
