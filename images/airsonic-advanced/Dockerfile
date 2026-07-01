# =============================================================================
# EVERGREEN HARDENED AIRSONIC-ADVANCED
# Generated from template - Version: 10.6.0
# Constraint: debian-slim - JRE required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=10.6.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
RUN mkdir -p /app || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/airsonic-advanced/airsonic-advanced/releases/download/v${VERSION}/airsonic.war -o /app/airsonic.war \
    echo "528f417e59499161ad7fd8b86d391e3c7eff70e0825465e315f86d3417664c69  /app/airsonic.war" | sha256sum -c  #


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/airsonic-advanced /var/cache/airsonic-advanced && chown -R 65532:65532 /var/log/airsonic-advanced /var/cache/airsonic-advanced 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 4040

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:4040"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "java -jar /app/airsonic-advanced-11.1.5.war"]
LABEL org.opencontainers.image.title="airsonic-advanced" \
      org.opencontainers.image.description="airsonic-advanced container image" \
      org.opencontainers.image.version="11.1.5" \
      org.opencontainers.image.vendor="Airsonic-Advanced" \
      org.opencontainers.image.source="https://github.com/airsonic-advanced/airsonic-advanced/releases" \
      evergreen.image.tier="3" \
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
