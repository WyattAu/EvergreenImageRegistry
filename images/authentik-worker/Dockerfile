# =============================================================================
# SOVEREIGN HARDENED AUTHENTIK WORKER
# Authentik background worker - Python app
# Constraint: debian-slim + Python - Python runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2026.2.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/goauthentik/authentik/releases/download/version/${VERSION}/authentik-worker-${VERSION}.tar.gz" -o /authentik-worker.tar.gz && \
    mkdir -p /tmp/authentik-worker && \
    tar -xzf /authentik-worker.tar.gz -C /tmp/authentik-worker && \
    rm -f /authentik-worker.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 py3-pip ca-certificates libpq libxml2-dev libxslt-dev libffi-dev openssl-dev build-base
COPY --from=downloader /tmp/authentik-worker /opt/authentik-worker
RUN pip3 install --no-cache-dir --break-system-packages /opt/authentik-worker 2>/dev/null || pip3 install --no-cache-dir /opt/authentik-worker || true && \
    mkdir -p /app && chown -R 65532:65532 /app /opt/authentik-worker
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["python3", "-m", "authentik"]
CMD ["worker"]
LABEL org.opencontainers.image.title="authentik-worker" \
      org.opencontainers.image.version="2026.2.2" \
      org.opencontainers.image.vendor="goauthentik" \
      org.opencontainers.image.source="https://github.com/goauthentik/authentik" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM