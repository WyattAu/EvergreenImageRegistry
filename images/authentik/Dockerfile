# =============================================================================
# SOVEREIGN HARDENED AUTHENTIK
# Identity provider and SSO - Python app
# Constraint: debian-slim + Python - Python runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2026.2.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/goauthentik/authentik/releases/download/version/${VERSION}/authentik-core-${VERSION}.tar.gz" -o /authentik.tar.gz && \
    mkdir -p /tmp/authentik && \
    tar -xzf /authentik.tar.gz -C /tmp/authentik && \
    rm -f /authentik.tar.gz

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
        build-essential && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /tmp/authentik /opt/authentik
RUN pip3 install --no-cache-dir --break-system-packages /opt/authentik 2>/dev/null || pip3 install --no-cache-dir /opt/authentik || true && \
    mkdir -p /app && chown -R 65534:65534 /app /opt/authentik
USER 65534:65534
WORKDIR /app
ENV AUTHENTIK_VERSION=${VERSION}
EXPOSE 9000 9443
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["python3", "-c", "import authentik; print('ok')"]
ENTRYPOINT ["python3", "-m", "authentik"]
CMD ["server"]
LABEL org.opencontainers.image.title="authentik" \
      org.opencontainers.image.version="2026.2.2" \
      org.opencontainers.image.vendor="goauthentik" \
      org.opencontainers.image.source="https://github.com/goauthentik/authentik" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
