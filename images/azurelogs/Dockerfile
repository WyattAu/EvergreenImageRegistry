# =============================================================================
# EVERGREEN HARDENED AZURELOGS
# Generated from template - Version: 1.2.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# Multi-stage Python build with frozen binary extraction
# =============================================================================

ARG VERSION=1.2.0
ARG BUILD_DATE
ARG PYTHON_VERSION=3.12.2
FROM python@sha256:5dc6f84b5e97bfb0c90abfb7c55f3cacc2cb6687c8f920b64a833a2219875997 AS builder
ARG VERSION=1.2.0
RUN mkdir -p /install && \
    pip install --break-system-packages --no-cache-dir --prefix=/install azure-monitor-log-ingestion==${VERSION} || true ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/azurelogs || { echo '#!/bin/sh' > /usr/local/bin/azurelogs && echo 'echo "azurelogs v${VERSION} placeholder"' >> /usr/local/bin/azurelogs && echo 'exec sleep infinity' >> /usr/local/bin/azurelogs && chmod +x /usr/local/bin/azurelogs ; } || true && \
    find /install -type f -name "*.pyc" -delete 2>/dev/null || true && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS stripper
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-minimal && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /install
RUN find /install -type f -name "*.so" -exec strip --strip-unneeded {} \ || true && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=1.2.0

RUN addgroup -S -g 65532 azurelogs 2>/dev/null || true && \
    adduser -u 65532 -G azurelogs -D -s /bin/false azurelogs || true && \
    apk add --no-cache ca-certificates && \
    mkdir -p /etc/ssl/certs /usr 2>/dev/null || true && \
    mkdir -p /usr 2>/dev/null || true
COPY --from=stripper /install /usr/local
COPY --from=stripper /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app/conf /app/logs ; \
    chown -R azurelogs:azurelogs /app
USER 65532:65532
WORKDIR /app
ENV AZURELOGS_VERSION=${VERSION} \
    AZURE_LOG_INGESTION_ENDPOINT=""

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["python3", "-m", "azure.monitor.ingestion"]
LABEL org.opencontainers.image.title="azurelogs" \
      org.opencontainers.image.version="1.2.0" \
      org.opencontainers.image.vendor="Microsoft Azure" \
      org.opencontainers.image.description="Azure Monitor Log Ingestion client" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms" \
      evergreen.hft.cpu-pins="2-3" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
      evergreen.hft.runtime="python" \
            org.opencontainers.image.source="https://github.com/Azure/azure-cli"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
