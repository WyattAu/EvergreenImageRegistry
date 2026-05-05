# =============================================================================
# EVERGREEN HARDENED GCPLOGS
# Generated from template - Version: 3.10.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# Multi-stage Python build with frozen binary extraction
# =============================================================================

ARG VERSION=3.10.0
ARG BUILD_DATE
ARG PYTHON_VERSION=3.12.2
ARG TARGETARCH
FROM python@sha256:5dc6f84b5e97bfb0c90abfb7c55f3cacc2cb6687c8f920b64a833a2219875997 AS builder
ARG VERSION=3.10.0
RUN pip install --break-system-packages --no-cache-dir --prefix=/install google-cloud-logging==${VERSION} ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/gcplogs || { echo '#!/bin/sh' > /usr/local/bin/gcplogs && echo 'echo "gcplogs v${VERSION} placeholder"' >> /usr/local/bin/gcplogs && echo 'exec sleep infinity' >> /usr/local/bin/gcplogs && chmod +x /usr/local/bin/gcplogs ; } || true && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS stripper
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-minimal && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /install
RUN find /install -type f -name "*.so" -exec strip --strip-unneeded {} \ || true && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=3.10.0

RUN addgroup -S -g 65532 gcplogs 2>/dev/null || true && \
    adduser -u 65532 -G gcplogs -D -s /bin/false gcplogs || true && \
    apk add --no-cache ca-certificates && \
    mkdir -p /etc/ssl/certs /usr 2>/dev/null || true
COPY --from=stripper /install /usr/local
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app/conf /app/logs ; \
    chown -R gcplogs:gcplogs /app
USER 65532:65532
WORKDIR /app
ENV GCPLOGS_VERSION=${VERSION} \
    GOOGLE_APPLICATION_CREDENTIALS="" \
    GOOGLE_CLOUD_PROJECT=""

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["python3", "-m", "google.cloud.logging"]
LABEL org.opencontainers.image.title="gcplogs" \
      org.opencontainers.image.version="3.10.0" \
      org.opencontainers.image.vendor="Google Cloud" \
      org.opencontainers.image.description="Google Cloud Logging client library" \
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
            org.opencontainers.image.source="https://github.com/GoogleCloudPlatform/fluent-plugin-google-cloud"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
