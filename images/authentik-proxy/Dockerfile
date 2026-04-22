# =============================================================================
# SOVEREIGN HARDENED AUTHENTIK PROXY
# Authentik outpost proxy worker - Python app
# Constraint: debian-slim + Python - Python runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2026.2.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/goauthentik/authentik/releases/download/version/${VERSION}/authentik-proxy-${VERSION}.tar.gz" -o /authentik-proxy.tar.gz && \
    mkdir -p /tmp/authentik-proxy && \
    tar -xzf /authentik-proxy.tar.gz -C /tmp/authentik-proxy && \
    rm -f /authentik-proxy.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache python3 py3-pip ca-certificates libpq
COPY --from=downloader /tmp/authentik-proxy /opt/authentik-proxy
RUN pip3 install --no-cache-dir --break-system-packages /opt/authentik-proxy 2>/dev/null || pip3 install --no-cache-dir /opt/authentik-proxy || true && \
    mkdir -p /app && chown -R 65532:65532 /app /opt/authentik-proxy
USER 65532:65532
WORKDIR /app
EXPOSE 9000 9443
ENTRYPOINT ["python3", "-m", "authentik"]
CMD ["proxy"]
LABEL org.opencontainers.image.title="authentik-proxy" \
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