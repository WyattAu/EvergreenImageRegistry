ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.7.0
ARG TARGETARCH
RUN mkdir -p /tmp/woodpecker-server || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/woodpecker-ci/woodpecker/releases/download/v${VERSION}/woodpecker-server_linux_${TARGETARCH}.tar.gz" \
    -o /tmp/archive.tar.gz && \
    echo "3ded2b21c58052b55c72948f5d215bba5be67443b2d5b87e14ae770bf77e881c  /tmp/archive.tar.gz" | sha256sum -c ; \
    tar -xzf /tmp/archive.tar.gz -C /tmp && \
    strip /tmp/woodpecker-server&& \
    chmod +x /tmp/woodpecker-server
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /tmp/woodpecker-server /usr/local/bin/woodpecker-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8000"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="woodpecker-ci" \
      org.opencontainers.image.description="Woodpecker CI Server - CI/CD server for Woodpecker CI" \
      org.opencontainers.image.version="2.7.0" \
      org.opencontainers.image.vendor="Woodpecker CI" \
      org.opencontainers.image.source="https://github.com/woodpecker-ci/woodpecker" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
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
