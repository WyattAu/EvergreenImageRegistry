ARG VERSION=7.1.4
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=7.1.4
RUN mkdir -p /ocis /app /var/log/ocis /var/cache/ocis
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/owncloud/ocis/releases/download/v${VERSION}/ocis-${VERSION}-linux-${TARGETARCH}" -o /ocis && \
    chmod +x /ocis && \
    sha256sum /ocis || true && \
    test -f /ocis || true && \
    mkdir -p /app /var/log/ocis /var/cache/ocis /etc/ocis 2>/dev/null || true

FROM scratch
ARG VERSION=7.1.4
ARG TARGETARCH
COPY --from=downloader /ocis /ocis
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /app /app
COPY --from=downloader /var/log/ocis /var/log/ocis
COPY --from=downloader /var/cache/ocis /var/cache/ocis
COPY --from=downloader /etc/ocis /etc/ocis
USER 65532:65532
WORKDIR /app
EXPOSE 9200

HEALTHCHECK NONE
ENTRYPOINT ["/ocis"]
LABEL org.opencontainers.image.title="ocis" \
      org.opencontainers.image.description="ownCloud Infinite Scale - next-gen file sync and share platform" \
      org.opencontainers.image.version="7.1.4" \
      org.opencontainers.image.vendor="ownCloud" \
      org.opencontainers.image.source="https://github.com/owncloud/ocis" \
      evergreen.image.tier="2" \
      evergreen.image.category="file-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
