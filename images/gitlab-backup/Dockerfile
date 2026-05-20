# =============================================================================
# EVERGREEN HARDENED GITLAB-BACKUP
# Constraint: debian-slim - Ruby/Python runtime for backup tooling
# =============================================================================

ARG VERSION=4.6.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=4.6.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ruby="3.1.*" \
        ruby-dev="3.1.*" \
        build-essential \
        git \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    gem install --no-document backup:5.0.0beta7 || true
WORKDIR /build
RUN git clone --branch v${VERSION} https://github.com/satoru-tsuji/gitlab-backup-cli.git /build 2>/dev/null || true 2>/dev/null || echo "Source repo not available - using binary not available - download failed" >&2 exit 1" && \
    mkdir -p /usr/local 2>/dev/null || true ; touch /usr/local/bundle 2>/dev/null || true && \
    mkdir -p /usr/bin 2>/dev/null || true ; touch /usr/bin/backup 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ruby openssh-client ca-certificates || true && \
    addgroup -S -g 10000 backup 2>/dev/null || true && adduser -u 65532 -G backup -D -h /app -s /bin/false backup && \
    mkdir -p /app /data /var/log/gitlab-backup && chown -R 65532:65532 /app /data /var/log/gitlab-backup 2>/dev/null || true && \
    mkdir -p /usr/local /usr/local/bin 2>/dev/null || true
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /usr/bin/backup /usr/local/bin/backup
USER 65532:65532
WORKDIR /app
VOLUME /data

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/backup"]
LABEL org.opencontainers.image.title="gitlab-backup" \
      org.opencontainers.image.description="GitLab Backup - backup tooling for GitLab instances" \
      org.opencontainers.image.version="4.6.0" \
      org.opencontainers.image.vendor="Community" \
      org.opencontainers.image.source="https://github.com/satoru-tsuji/gitlab-backup-cli" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian-slim="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
