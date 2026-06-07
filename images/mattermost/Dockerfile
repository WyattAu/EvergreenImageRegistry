ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=11.6.2
RUN mkdir -p /opt/mattermost || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tar && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://releases.mattermost.com/${VERSION}/mattermost-${VERSION}-linux-${TARGETARCH}.tar.gz" -o /mattermost.tar.gz ; \
    echo "61e0a677faf07dbc0513b7e419227611eb97d5f278323d6741b1b17c615076d6  /mattermost.tar.gz" | sha256sum -c ; \
    mkdir -p /opt ; \
    if [ -f /mattermost.tar.gz ]; then tar -xzf /mattermost.tar.gz -C /opt && rm -f /mattermost.tar.gz ; fi ; \
    ln -sf /opt/mattermost-${VERSION} /opt/mattermost 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates tzdata
COPY --from=downloader /opt/mattermost /opt/mattermost
RUN addgroup -S -g 65532 mattermost 2>/dev/null || true && \
    adduser -u 65532 -G mattermost -D -D -h /opt/mattermost -s /bin/false mattermost 2>/dev/null || true && \
    mkdir -p /opt/mattermost-src/data /opt/mattermost/logs /opt/mattermost/plugins /opt/mattermost/client/plugins ; \
    chown -R 65532:65532 /opt/mattermost
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/mattermost
EXPOSE 8065

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8065"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="mattermost" \
      org.opencontainers.image.description="mattermost container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/mattermost" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="collaboration" \
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
