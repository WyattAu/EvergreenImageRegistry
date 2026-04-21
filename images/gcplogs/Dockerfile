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
RUN pip install --no-cache-dir --prefix=/install google-cloud-logging==${VERSION}
RUN find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

FROM debian:bookworm-20240101-slim AS stripper
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-minimal && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /install
RUN find /install -type f -name "*.so" -exec strip --strip-unneeded {} \; 2>/dev/null || true

FROM debian:bookworm-20240101-slim
RUN groupadd -g 65534 gcplogs && \
    useradd -m -u 65534 -g gcplogs -s /usr/sbin/nologin gcplogs
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-minimal ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=stripper /install /usr/local
COPY --from=stripper /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app/conf /app/logs && \
    chown -R gcplogs:gcplogs /app
USER 65534:65534
WORKDIR /app
ENV GCPLOGS_VERSION=${VERSION} \
    GOOGLE_APPLICATION_CREDENTIALS="" \
    GOOGLE_CLOUD_PROJECT=""
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/python3", "-m", "pip", "show", "google-cloud-logging"]
ENTRYPOINT ["python3", "-m", "google.cloud.logging"]
LABEL org.opencontainers.image.title="gcplogs" \
      org.opencontainers.image.version="3.10.0" \
      org.opencontainers.image.vendor="Google Cloud" \
      org.opencontainers.image.description="Google Cloud Logging client library" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
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
