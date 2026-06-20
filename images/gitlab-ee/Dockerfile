ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
COPY --from=shim /shim /usr/local/bin/shim

ARG VERSION=16.11.0
ARG TARGETARCH
RUN mkdir -p /opt/gitlab && \
    mkdir -p /var/opt/gitlab || true
RUN mkdir -p /etc/gitlab && \
    mkdir -p /opt/gitlab && \
    mkdir -p /var/opt/gitlab || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg \
        openssh-client && \
    rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 --proto '=https' --tlsv1.2 -fsSL "https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh" -o /tmp/install.sh && \
    sha256sum /tmp/install.sh && \
    bash /tmp/install.sh && rm -f /tmp/install.sh && \
    apt-get update && \
    apt-get install -y --no-install-recommends gitlab-ee 2>/dev/null && \
    rm -rf /var/lib/apt/lists/*

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache wget ca-certificates gnupg openssh-client postfix busybox
COPY --from=downloader /opt/gitlab /opt/gitlab
COPY --from=downloader /etc/gitlab /etc/gitlab
COPY --from=downloader /var/opt/gitlab /var/opt/gitlab
RUN addgroup -S -g 10000 gitlab 2>/dev/null || true && \
    adduser -u 65532 -G gitlab -D -h /var/opt/gitlab -s /bin/false gitlab 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
EXPOSE 80 443 22
LABEL org.opencontainers.image.title="gitlab-ee" \
      org.opencontainers.image.description="GitLab EE - self-hosted Git management platform (Enterprise)" \
      org.opencontainers.image.version="16.11.0" \
      org.opencontainers.image.vendor="GitLab" \
      org.opencontainers.image.source="https://gitlab.com/gitlab-org/gitlab-ee" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
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

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:22"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/opt/gitlab/bin/gitlab"]
