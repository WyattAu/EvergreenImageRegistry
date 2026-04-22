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
        build-essential \
        git \
        curl="7.88.1-*" \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN gem install --no-document backup:5.0.0beta7
WORKDIR /build
RUN git clone --depth 1 --branch v${VERSION} https://github.com/satoru-tsuji/gitlab-backup-cli.git /build 2>/dev/null || true

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ruby="3.1.*" \
        openssh-client \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd -r -g 65534 backup && useradd -r -u 65534 -g backup -d /app -s /usr/sbin/nologin backup
RUN mkdir -p /app /data /var/log/gitlab-backup && chown -R 65534:65534 /app /data /var/log/gitlab-backup
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /usr/bin/backup /usr/local/bin/backup 2>/dev/null || true
USER 65534:65534
WORKDIR /app
VOLUME /data
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["ruby", "-v"]
ENTRYPOINT ["/usr/local/bin/backup"]
LABEL org.opencontainers.image.title="gitlab-backup" \
      org.opencontainers.image.description="GitLab Backup - backup tooling for GitLab instances" \
      org.opencontainers.image.version="4.6.0" \
      org.opencontainers.image.vendor="Community" \
      org.opencontainers.image.source="https://github.com/satoru-tsuji/gitlab-backup-cli" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
