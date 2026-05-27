ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS downloader
ARG TARGETARCH
ARG VERSION=1.22.0
RUN apk add --no-cache curl ca-certificates xz && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://dl.gitea.io/gitea/${VERSION}/gitea-${VERSION}-linux-${TARGETARCH}.xz" \
    -o /tmp/gitea.xz && \
    echo "b58e02e9e863a0191f26a26fbe6ef7e24c4c9917940c21957e6713cadcc5b9fd  /tmp/gitea.xz" | sha256sum -c && \
    xz -d /tmp/gitea.xz && \
    chmod +x /tmp/gitea && \
    strip /tmp/gitea
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=1.22.0
RUN apk add --no-cache ca-certificates git tzdata && \
    adduser -D -u 65532 git 2>/dev/null || true && \
    mkdir -p /app /var/lib/gitea /var/log/gitea /etc/gitea /var/cache/gitea 2>/dev/null || true
COPY --from=downloader /tmp/gitea /usr/local/bin/gitea
RUN chown -R 65532:65532 /app /var/lib/gitea /var/log/gitea /etc/gitea /var/cache/gitea 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 3000 22

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:22/ || exit 1
ENTRYPOINT ["/usr/local/bin/gitea"]
CMD ["web", "-c", "/etc/gitea/app.ini"]
LABEL org.opencontainers.image.title="source-control" \
      org.opencontainers.image.description="Source control management - Gitea lightweight Git server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Gitea" \
      org.opencontainers.image.source="https://about.gitea.com/" \
      evergreen.image.tier="2" \
      evergreen.image.category="scm" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.wolfi="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
