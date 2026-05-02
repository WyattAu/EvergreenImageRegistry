ARG VERSION=latest

FROM ghcr.io/prometheus-community/gitlab-exporter:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/gitlab-exporter /var/cache/gitlab-exporter 2>/dev/null || true


FROM scratch
COPY --from=upstream /gitlab-exporter /usr/local/bin/gitlab-exporter
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/gitlab-exporter /var/log/gitlab-exporter
COPY --from=builder /var/cache/gitlab-exporter /var/cache/gitlab-exporter

WORKDIR /app

EXPOSE 9171
EXPOSE 9101

LABEL org.opencontainers.image.title="gitlab-exporter" org.opencontainers.image.description="GitLab Exporter - Prometheus exporter for GitLab metrics" org.opencontainers.image.version="0.8.0" org.opencontainers.image.vendor="Prometheus Community" org.opencontainers.image.source="https://github.com/prometheus-community/gitlab-exporter" sovereign.image.tier="2" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["gitlab-exporter"]
