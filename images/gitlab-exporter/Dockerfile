FROM debian:bookworm-slim AS downloader
ARG VERSION=0.8.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus-community/gitlab-exporter/releases/download/v${VERSION}/gitlab-exporter_${VERSION}_linux_amd64" -o /tmp/gitlab-exporter && \
    chmod +x /tmp/gitlab-exporter && strip /tmp/gitlab-exporter || true
RUN test -f /tmp/gitlab-exporter && test -s /tmp/gitlab-exporter || { echo "ERROR: gitlab-exporter binary not downloaded" >&2; exit 1; }

FROM scratch
COPY --from=downloader /tmp/gitlab-exporter /usr/local/bin/gitlab-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 9171
LABEL org.opencontainers.image.title="gitlab-exporter" \
      org.opencontainers.image.description="GitLab Exporter - Prometheus exporter for GitLab metrics" \
      org.opencontainers.image.version="0.8.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.source="https://github.com/prometheus-community/gitlab-exporter" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
ENTRYPOINT ["gitlab-exporter"]
