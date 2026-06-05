# =============================================================================
# EVERGREEN HARDENED GITEA
# Generated from template - Version: 1.21.10
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=1.21.10
ARG BUILD_DATE
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.3.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS downloader
ARG TARGETARCH
# hadolint ignore=DL3018
RUN apk add --no-cache wget ca-certificates && \
    ARCH=$(case ${TARGETARCH} in amd64) echo "amd64" ;; arm64) echo "arm64" ;; *) echo "amd64" ;; esac) && \
    wget -t 3 -T 10 -qO /gitea "https://github.com/go-gitea/gitea/releases/download/v1.21.10/gitea-1.21.10-linux-${ARCH}" && chmod +x /gitea 2>/dev/null && \
    echo "17eb858f3ef2b7cdb649286e6a9cc050f9d949606327a7d6f27aaba49fc3b492  /gitea" | sha256sum -c  #
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS runtime
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN adduser -D -u 65532 git 2>/dev/null || true && \
    mkdir -p /app /var/log/gitea /var/cache/gitea 2>/dev/null || true
USER git
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
# hadolint ignore=DL3023
COPY --from=downloader /gitea /usr/local/bin/gitea
EXPOSE 3000 22

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="gitea" \
      org.opencontainers.image.description="Gitea - lightweight self-hosted Git service" \
      org.opencontainers.image.version="1.21.10" \
      org.opencontainers.image.vendor="Gitea" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.wolfi="true" \
            org.opencontainers.image.source="https://github.com/go-gitea/gitea"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
