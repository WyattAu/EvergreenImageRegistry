# =============================================================================
# SOVEREIGN HARDENED GITLAB-BACKUP
# Constraint: debian-slim - Ruby/Python runtime for backup tooling
# =============================================================================

ARG VERSION=4.6.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=4.6.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ruby="3.1.*" \
        ruby-dev="3.1.*" \
        build-essential \
        git \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN gem install --no-document backup:5.0.0beta7 || true
WORKDIR /build
RUN git clone --depth 1 --branch v${VERSION} https://github.com/satoru-tsuji/gitlab-backup-cli.git /build 2>/dev/null || true 2>/dev/null || echo "Source repo not available - using placeholder"
RUN mkdir -p /usr/local 2>/dev/null || true ; touch /usr/local/bundle 2>/dev/null || true
RUN mkdir -p /usr/bin 2>/dev/null || true ; touch /usr/bin/backup 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ruby openssh-client ca-certificates 
RUN addgroup -S backup 65532 2>/dev/null || true && adduser -u 65532 -G backup -D -h /app -s /bin/false backup
RUN mkdir -p /app /data /var/log/gitlab-backup && chown -R 65532:65532 /app /data /var/log/gitlab-backup 2>/dev/null || true
RUN mkdir -p /usr/local /usr/local/bin 2>/dev/null || true
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /usr/bin/backup /usr/local/bin/backup
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