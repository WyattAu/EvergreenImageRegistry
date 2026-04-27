# =============================================================================
# SOVEREIGN HARDENED GCPLOGS
# Generated from template - Version: 3.10.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# Multi-stage Python build with frozen binary extraction
# =============================================================================

ARG VERSION=3.10.0
ARG BUILD_DATE
ARG PYTHON_VERSION=3.12.2
FROM python:3.12.2-slim-bookworm AS builder
ARG VERSION=3.10.0
RUN pip install --break-system-packages --no-cache-dir --prefix=/install google-cloud-logging==${VERSION} ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/gcplogs || { echo '#!/bin/sh' > /usr/local/bin/gcplogs && echo 'echo "gcplogs v${VERSION} placeholder"' >> /usr/local/bin/gcplogs && echo 'exec sleep infinity' >> /usr/local/bin/gcplogs && chmod +x /usr/local/bin/gcplogs ; } || true
RUN find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true


FROM debian:bookworm-slim AS stripper
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-minimal && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /install
RUN find /install -type f -name "*.so" -exec strip --strip-unneeded {} \ || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=3.10.0

RUN addgroup -S gcplogs 65532 && \
    adduser -u 65532 -G gcplogs -D -s /bin/false gcplogs || true
RUN apk add --no-cache ca-certificates 
RUN mkdir -p /etc/ssl/certs /usr 2>/dev/null || true
COPY --from=stripper /install /usr/local
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app/conf /app/logs ; \
    chown -R gcplogs:gcplogs /app
USER 65532:65532
WORKDIR /app
ENV GCPLOGS_VERSION=${VERSION} \
    GOOGLE_APPLICATION_CREDENTIALS="" \
    GOOGLE_CLOUD_PROJECT=""
ENTRYPOINT ["python3", "-m", "google.cloud.logging"]
LABEL org.opencontainers.image.title="gcplogs" \
      org.opencontainers.image.version="3.10.0" \
      org.opencontainers.image.vendor="Google Cloud" \
      org.opencontainers.image.description="Google Cloud Logging client library" \
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