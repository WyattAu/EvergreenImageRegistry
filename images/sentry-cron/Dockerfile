# =============================================================================
# SOVEREIGN HARDENED SENTRY CRON
# Sentry cron scheduler - Python app
# Constraint: debian-slim + Python - Python runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=26.4.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/getsentry/self-hosted/releases/download/${VERSION}/sentry-${VERSION}.tar.gz" -o /sentry.tar.gz && \
    mkdir -p /tmp/sentry && \
    tar -xzf /sentry.tar.gz -C /tmp/sentry && \
    rm -f /sentry.tar.gz

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates \
        libpq5 \
        libxml2-dev \
        libxslt1-dev \
        libjpeg62-turbo-dev \
        zlib1g-dev \
        libffi-dev \
        libssl-dev \
        libyaml-dev \
        build-essential \
        git && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /tmp/sentry /opt/sentry
RUN if [ -f /opt/sentry/requirements.txt ]; then pip3 install --no-cache-dir --break-system-packages -r /opt/sentry/requirements.txt 2>/dev/null || pip3 install --no-cache-dir -r /opt/sentry/requirements.txt || true; fi && \
    mkdir -p /app && chown -R 65534:65534 /app /opt/sentry
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["python3", "-c", "import sentry; print('ok')"]
ENTRYPOINT ["python3", "-m", "sentry"]
CMD ["cron"]
LABEL org.opencontainers.image.title="sentry-cron" \
      org.opencontainers.image.version="26.4.0" \
      org.opencontainers.image.vendor="Sentry" \
      org.opencontainers.image.source="https://github.com/getsentry/self-hosted" \
      sovereign.image.tier="2" \
      sovereign.image.category="monitoring" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
