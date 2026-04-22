# =============================================================================
# SOVEREIGN HARDENED GITLAB-OPERATOR
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=0.8.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://gitlab.com/api/v4/projects/gitlab-org%2Fcloud-native%2Fgitlab-operator/packages/generic/gitlab-operator/0.8.0/gitlab-operator-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/gitlab-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/gitlab-operator", "--version"]
ENTRYPOINT ["/usr/local/bin/gitlab-operator"]
LABEL org.opencontainers.image.title="gitlab-operator"       org.opencontainers.image.description="GitLab Operator - Kubernetes operator for GitLab"       org.opencontainers.image.version="0.8.0"       org.opencontainers.image.vendor="GitLab"       org.opencontainers.image.source="https://gitlab.com/gitlab-org/cloud-native/gitlab-operator"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
