ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=5.7.6
ARG TARGETARCH
RUN apk add --no-cache knot-resolver 2>/dev/null || apk add --no-cache bind-tools 2>/dev/null knot-resolver-utils ca-certificates && \
    addgroup -S -g 10000 knot 2>/dev/null || true && \
    adduser -u 65532 -G knot -D -h /app -s /bin/false knot 2>/dev/null || true && \
    mkdir -p /app /var/log/knot-resolver /var/lib/knot-resolver /etc/knot-resolver /run/knot 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/knot-resolver /var/lib/knot-resolver /etc/knot-resolver /run/knot 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 53 53/udp 8453

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:53"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "kresd", "--", "-c", "/etc/knot-resolver/knot.conf"]
LABEL org.opencontainers.image.title="knot-resolver" \
      org.opencontainers.image.version="5.7.6" \
      org.opencontainers.image.vendor="CZ.NIC" \
      org.opencontainers.image.source="https://github.com/CZ-NIC/knot-resolver" \
      org.opencontainers.image.description="Full-featured DNS recursive resolver" \
      evergreen.image.tier="1" \
      evergreen.image.category="dns" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
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
