# =============================================================================
# SOVEREIGN HARDENED GITLAB-EXPORTER
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=0.8.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus-community/gitlab-exporter/releases/download/v0.8.0/gitlab-exporter_0.8.0_linux_amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/gitlab-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
WORKDIR /app
EXPOSE 9171
LABEL org.opencontainers.image.title="gitlab-exporter"       org.opencontainers.image.description="GitLab Exporter - Prometheus exporter for GitLab metrics"       org.opencontainers.image.version="0.8.0"       org.opencontainers.image.vendor="Prometheus Community"       org.opencontainers.image.source="https://github.com/prometheus-community/gitlab-exporter"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM