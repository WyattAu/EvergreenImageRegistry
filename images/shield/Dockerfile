
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=8.6.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/starkandwayne/shield/releases/download/v${VERSION}/shield-linux-${TARGETARCH} -o /shield ; \
    echo "ca9c1fcb7bf3e77bb22d5777aab791a5cd3119b96bd79d6f674ff042cbbe7168  /shield" | sha256sum -c ; \
    chmod +x /shield && \
    strip --strip-all /shield 2>/dev/null && { echo "Binary not available - download failed" >&2; exit 1; }



FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /shield /shield
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8443"]

ENTRYPOINT ["/shim", "run"]
CMD ["-c", "/shield", "--", "server", "-c", "/app/shield.yml"]
LABEL org.opencontainers.image.title="shield" \
      org.opencontainers.image.description="shield container image" \
      org.opencontainers.image.version="8.6.0" \
      org.opencontainers.image.vendor="Stark & Wayne" \
      org.opencontainers.image.source="https://github.com/starkandwayne/shield" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
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
