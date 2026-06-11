ARG TARGETARCH

ARG VERSION=15.0.2

ARG SHIM_VERSION=v1.0.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS downloader
ARG VERSION
RUN apk add --no-cache wget ca-certificates git && \
    mkdir -p /app && \
    wget -t 3 -T 30 -qO /app/forgejo "https://code.forgejo.org/forgejo/forgejo/releases/download/v${VERSION}/forgejo-${VERSION}-linux-amd64" && \
    chmod +x /app/forgejo && \
    test -s /app/forgejo

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION
RUN apk add --no-cache bash git openssh-keygen ca-certificates && \
    addgroup -g 1000 git && \
    adduser -D -u 1000 -G git -h /data git && \
    mkdir -p /data /etc/forgejo /var/log/forgejo /var/cache/forgejo /data/git/repositories /data/lfs /data/log && \
    chown -R git:git /data
WORKDIR /app
ENV FORGEJO_WORK_DIR=/data
ENV GITEA_WORK_DIR=/data
COPY --from=downloader /app/forgejo /usr/local/bin/forgejo
COPY app.ini /etc/forgejo/app.ini
RUN chmod 660 /etc/forgejo/app.ini && chown 1000:1000 /etc/forgejo/app.ini && chown -R 1000:1000 /app
EXPOSE 3000 22 9101

CMD ["--", "web"]

USER 1000:1000
ENV SHIM_METRICS_ENABLED="true"
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "forgejo"]
LABEL org.opencontainers.image.title="forgejo" \
      org.opencontainers.image.description="Forgejo - community-owned lightweight software forge" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Forgejo" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      org.opencontainers.image.source="https://codeberg.org/forgejo/forgejo"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
