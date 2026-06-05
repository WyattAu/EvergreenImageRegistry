ARG VERSION=2.3.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.3.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/go-vikunja/vikunja/releases/download/v${VERSION}/vikunja-v${VERSION}-linux-${TARGETARCH}-full.zip" \
    -o /vikunja.zip 2>/dev/null || true && \
    mkdir -p /tmp/vikunja && \
    unzip -o /vikunja.zip -d /tmp/vikunja 2>/dev/null && \
    cp /tmp/vikunja/vikunja /vikunja 2>/dev/null || find /tmp/vikunja -name 'vikunja' -type f -exec cp {} /vikunja \; 2>/dev/null && \
    chmod +x /vikunja 2>/dev/null ; && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/vikunja /var/cache/vikunja 2>/dev/null

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /vikunja /vikunja
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vikunja /var/log/vikunja
COPY --from=builder /var/cache/vikunja /var/cache/vikunja
USER 65532:65532
WORKDIR /app
EXPOSE 3456

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:3456"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="vikunja" \
      org.opencontainers.image.description="vikunja container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Vikunja" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/go-vikunja/vikunja"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
