# =============================================================================
# SOVEREIGN HARDENED GITLAB-CE
# Constraint: debian-slim - complex omnibus package requires full runtime
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

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl="7.88.1-*" \
        ca-certificates \
        gnupg \
        openssh-client \
        postfix="3.7.*" \
        cron="3.0pl1-*" && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/gitlab /opt/gitlab
COPY --from=downloader /etc/gitlab /etc/gitlab
COPY --from=downloader /var/opt/gitlab /var/opt/gitlab
RUN groupadd -r -g 65534 gitlab 2>/dev/null || true && \
    useradd -r -u 65534 -g gitlab -d /var/opt/gitlab -s /usr/sbin/nologin gitlab 2>/dev/null || true
USER 65534:65534
EXPOSE 80 22 443
HEALTHCHECK --interval=30s --timeout=10s --start-period=300s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:80/api/v4/health"]
LABEL org.opencontainers.image.title="gitlab-ce" \
      org.opencontainers.image.description="GitLab CE - self-hosted Git management platform" \
      org.opencontainers.image.version="17.6.0" \
      org.opencontainers.image.vendor="GitLab" \
      org.opencontainers.image.source="https://gitlab.com/gitlab-org/gitlab-ce" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
