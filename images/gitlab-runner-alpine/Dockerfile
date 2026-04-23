# =============================================================================
# SOVEREIGN HARDENED GITLAB-RUNNER-ALPINE
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=16.11.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://gitlab-runner-downloads.s3.amazonaws.com/v16.11.0/binaries/gitlab-runner-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/gitlab-runner
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
WORKDIR /app
EXPOSE 8093
LABEL org.opencontainers.image.title="gitlab-runner-alpine"       org.opencontainers.image.description="GitLab Runner (scratch) - CI/CD runner for GitLab, minimal scratch image"       org.opencontainers.image.version="16.11.0"       org.opencontainers.image.vendor="GitLab"       org.opencontainers.image.source="https://gitlab.com/gitlab-org/gitlab-runner"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM