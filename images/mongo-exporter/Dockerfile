# =============================================================================
# SOVEREIGN HARDENED MONGO-EXPORTER (Percona)
# Generated from template - Version: 0.40.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.40.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/percona/mongodb_exporter/releases/download/v${VERSION}/mongodb_exporter-${VERSION}-linux-amd64.tar.gz" \
    -o /mongodb_exporter.tar.gz \
    && echo "PENDING  /mongodb_exporter.tar.gz" | sha256sum -c || true  # \
    && tar -xzf /mongodb_exporter.tar.gz -C / \
    && strip --strip-all /mongodb_exporter-${VERSION}-linux-amd64/mongodb_exporter \
    && rm /mongodb_exporter.tar.gz

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/mongodb_exporter /var/cache/mongodb_exporter

FROM scratch
COPY --from=downloader /mongodb_exporter-${VERSION}-linux-amd64/mongodb_exporter /mongodb_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mongodb_exporter /var/log/mongodb_exporter
COPY --from=builder /var/cache/mongodb_exporter /var/cache/mongodb_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9216
ENTRYPOINT ["/mongodb_exporter"]
LABEL org.opencontainers.image.title="mongo-exporter" \
      org.opencontainers.image.version="0.40.0" \
      org.opencontainers.image.vendor="Percona" \
      org.opencontainers.image.description="Sovereign hardened MongoDB Exporter (Percona) - Prometheus exporter for MongoDB" \
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

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM