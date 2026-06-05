ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.6.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/letsencrypt/unbound_exporter/releases/download/v${VERSION}/unbound_exporter-v${VERSION}.x86_64.deb -o /unbound_exporter.deb && \
    echo "4f61876a292b49f918baf6b6b57d17dcf94f97513787282b0dadb88b95084890  /unbound_exporter.deb" | sha256sum -c ; \
    cd /tmp && ar -x /unbound_exporter.deb && tar -xzf data.tar.gz -C / && rm -f /unbound_exporter.deb data.tar.gz control.tar.gz debian-binary && \
    chmod +x /usr/bin/unbound_exporter ; \binary not available - download failed" >&2"' >> /usr/bin/unbound_exporter && echo 'exit 1' >> /usr/bin/unbound_exporter && chmod +x /usr/bin/unbound_exporter; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/unbound_exporter /var/cache/unbound_exporter 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /usr/bin/unbound_exporter /unbound_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/unbound_exporter /var/log/unbound_exporter
COPY --from=builder /var/cache/unbound_exporter /var/cache/unbound_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9167

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9167"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="unbound-exporter" \
      org.opencontainers.image.description="unbound-exporter container image" \
      org.opencontainers.image.version="0.6.0" \
      org.opencontainers.image.vendor="Let's Encrypt" \
      org.opencontainers.image.source="https://github.com/letsencrypt/unbound_exporter" \
      evergreen.image.tier="1" \
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
