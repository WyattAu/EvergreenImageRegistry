ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=1.0.0
ARG TARGETARCH
RUN apk add --no-cache nodejs-20 npm ca-certificates && \
    npm install -g @worldsibu/convector-platform@${VERSION} 2>/dev/null && \
    addgroup -S -g 10000 convector 2>/dev/null || true && \
    adduser -u 65532 -G convector -D -h /app -s /bin/false convector 2>/dev/null || true && \
    mkdir -p /app /var/log/convector 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/convector 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
ENV NODE_ENV="production"
EXPOSE 8008

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8008"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "node", "--", "[]"]
LABEL org.opencontainers.image.title="convector" \
      org.opencontainers.image.description="Convector - smart contract framework tools" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="worldsibu" \
      org.opencontainers.image.source="https://github.com/worldsibu/convector-platform" \
      evergreen.image.tier="3" \
      evergreen.image.category="blockchain" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
