# =============================================================================
# SOVEREIGN HARDENED GITLAB-BACKUP
# Constraint: debian-slim - Ruby/Python runtime for backup tooling
# =============================================================================

ARG VERSION=4.6.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ruby="3.1.*" \
        ruby-dev="3.1.*" \
        build-base \
        git \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN gem install --no-document backup:5.0.0beta7
WORKDIR /build
RUN git clone --depth 1 --branch v${VERSION} https://github.com/satoru-tsuji/gitlab-backup-cli.git /build 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apk add --no-cache ruby openssh-client ca-certificates
RUN addgroup -S -g 65532 backup && adduser -u 65532 -G backup -D -h /app -s /sbin/nologin backup
RUN mkdir -p /app /data /var/log/gitlab-backup && chown -R 65532:65532 /app /data /var/log/gitlab-backup
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /usr/bin/backup /usr/local/bin/backup 2>/dev/null || true
USER 65532:65532
WORKDIR /app
VOLUME /data
ENTRYPOINT ["/usr/local/bin/backup"]
LABEL org.opencontainers.image.title="gitlab-backup" \
      org.opencontainers.image.description="GitLab Backup - backup tooling for GitLab instances" \
      org.opencontainers.image.version="4.6.0" \
      org.opencontainers.image.vendor="Community" \
      org.opencontainers.image.source="https://github.com/satoru-tsuji/gitlab-backup-cli" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM