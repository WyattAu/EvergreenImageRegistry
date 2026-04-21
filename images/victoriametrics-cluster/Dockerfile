# =============================================================================
# SOVEREIGN HARDENED VICTORIAMETRICS-CLUSTER
# Generated from template - Version: 1.97.0
# Cluster variant: vminsert, vmselect, vmstorage
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.97.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.97.0/victoria-metrics-linux-amd64-v1.97.0-cluster.tar.gz" -o /vm-cluster.tar.gz && \
    tar -xzf /vm-cluster.tar.gz -C /tmp && rm /vm-cluster.tar.gz && \
    strip --strip-all /tmp/vminsert-prod && \
    strip --strip-all /tmp/vmselect-prod && \
    strip --strip-all /tmp/vmstorage-prod && \
    mv /tmp/vminsert-prod /vminsert && \
    mv /tmp/vmselect-prod /vmselect && \
    mv /tmp/vmstorage-prod /vmstorage

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/lib/victoriametrics /var/log/victoriametrics

FROM scratch
COPY --from=downloader /vminsert /vminsert
COPY --from=downloader /vmselect /vmselect
COPY --from=downloader /vmstorage /vmstorage
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/lib/victoriametrics /var/lib/victoriametrics
COPY --from=builder /var/log/victoriametrics /var/log/victoriametrics
USER 65534:65534
WORKDIR /app
EXPOSE 8480
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/vmstorage", "--version"]
ENTRYPOINT ["/vmstorage"]
LABEL org.opencontainers.image.title="victoriametrics-cluster" \
      org.opencontainers.image.version="1.97.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      sovereign.image.tier="1" \
      sovereign.image.category="tsdb" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"
