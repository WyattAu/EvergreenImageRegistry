# =============================================================================
# SOVEREIGN HARDENED PGBOUNCER-EXPORTER
# Generated from template - Version: 0.11.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.11.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/prometheus-community/pgbouncer_exporter/releases/download/v${VERSION}/pgbouncer_exporter-${VERSION}-linux-amd64.tar.gz" \
    -o /pgbouncer_exporter.tar.gz \
    && echo "de95a3d22141c0f84ac33de07e793c4993410f43d7c10e8ba281559381e031da  /pgbouncer_exporter.tar.gz" | sha256sum -c - \
    && tar -xzf /pgbouncer_exporter.tar.gz -C / \
    && strip --strip-all /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter \
    && rm /pgbouncer_exporter.tar.gz

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/pgbouncer_exporter /var/cache/pgbouncer_exporter

FROM scratch
COPY --from=downloader /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter /pgbouncer_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pgbouncer_exporter /var/log/pgbouncer_exporter
COPY --from=builder /var/cache/pgbouncer_exporter /var/cache/pgbouncer_exporter
USER 65534:65534
WORKDIR /app
EXPOSE 9127
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/pgbouncer_exporter", "--version"]
ENTRYPOINT ["/pgbouncer_exporter"]
LABEL org.opencontainers.image.title="pgbouncer-exporter" \
      org.opencontainers.image.version="0.11.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Sovereign hardened PgBouncer Exporter - Prometheus exporter for PgBouncer" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"
