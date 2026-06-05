ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=4.13.1
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/zitadel/zitadel/releases/download/v${VERSION}/zitadel-linux-${TARGETARCH}.tar.gz -o /zitadel.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/zitadel/zitadel/releases/download/v${VERSION}/checksums.txt -o /checksums.txt && \
    grep "zitadel-linux-${TARGETARCH}.tar.gz" /checksums.txt | sha256sum -c ; [ -f /zitadel.tar.gz ] && \
    [ -f /zitadel.tar.gz ] && tar -xzf /zitadel.tar.gz -C /tmp/ ; \
    strip --strip-all /tmp/zitadel 2>/dev/null&& \
    mv /tmp/zitadel /zitadel && \
    rm -rf /zitadel.tar.gz /checksums.txt /tmp/* && { echo "Binary not available - download failed" >&2; exit 1; }
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /zitadel /zitadel
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="zitadel" \
      org.opencontainers.image.description="zitadel container image" \
      org.opencontainers.image.version="4.13.1" \
      org.opencontainers.image.vendor="ZITADEL" \
      org.opencontainers.image.source="https://github.com/zitadel/zitadel" \
      evergreen.image.tier="2" \
      evergreen.image.category="identity" \
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
STOPSIGNAL SIGTERM
