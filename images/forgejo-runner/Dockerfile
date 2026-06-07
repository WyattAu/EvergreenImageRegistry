ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=12.10.1
RUN mkdir -p /tmp && touch /tmp/forgejo-runner
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://code.forgejo.org/forgejo/runner/releases/download/v${VERSION}/forgejo-runner-${VERSION}-linux-${TARGETARCH}" \
    -o /tmp/forgejo-runner && \
    chmod +x /tmp/forgejo-runner && \
    strip /tmp/forgejo-runner
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /tmp/forgejo-runner /usr/local/bin/forgejo-runner
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8088

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8088"]

ENTRYPOINT ["/shim", "run"]
CMD ["-c", "/usr/local/bin/forgejo-runner", "--", "daemon"]
LABEL org.opencontainers.image.title="forgejo-runner" \
      org.opencontainers.image.description="Forgejo Act Runner - CI/CD runner for Forgejo" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Forgejo" \
      org.opencontainers.image.source="https://codeberg.org/forgejo/runner" \
      evergreen.image.tier="2" \
      evergreen.image.category="ci" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
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
