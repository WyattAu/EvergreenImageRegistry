# =============================================================================
# SOVEREIGN HARDENED GITLAB-GEO
# Constraint: debian-slim - omnibus package for geo replication
# =============================================================================

ARG VERSION=17.6.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl="7.88.1-*" \
        ca-certificates \
        gnupg \
        openssh-client && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh" | bash && \
    apt-get update && \
    apt-get install -y --no-install-recommends gitlab-ce=${VERSION}-ce.0 && \
    rm -rf /var/lib/apt/lists/*

FROM cgr.dev/chainguard/wolfi-base:latest

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apk add --no-cache curl ca-certificates gnupg openssh-client postgresql-client
COPY --from=downloader /opt/gitlab /opt/gitlab
COPY --from=downloader /etc/gitlab /etc/gitlab
COPY --from=downloader /var/opt/gitlab /var/opt/gitlab
RUN groupadd -r -g 65532 gitlab 2>/dev/null || true && \
    useradd -r -u 65532 -g gitlab -d /var/opt/gitlab -s /usr/sbin/nologin gitlab 2>/dev/null || true
USER 65532:65532
EXPOSE 80 443
LABEL org.opencontainers.image.title="gitlab-geo" \
      org.opencontainers.image.description="GitLab Geo - geo-replication node for GitLab" \
      org.opencontainers.image.version="17.6.0" \
      org.opencontainers.image.vendor="GitLab" \
      org.opencontainers.image.source="https://gitlab.com/gitlab-org/gitlab-ce" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true" \
      sovereign.image.variant="geo"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM