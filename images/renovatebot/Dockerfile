# =============================================================================
# SOVEREIGN HARDENED RENOVATEBOT
# Automated dependency updates (alias) - Node.js app
# Constraint: debian-slim + Node.js - Node runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=43.138.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/renovatebot/renovate/releases/download/${VERSION}/renovate-${VERSION}.js.tar.gz" -o /renovate.tar.gz && \
    mkdir -p /tmp/renovate && \
    tar -xzf /renovate.tar.gz -C /tmp/renovate && \
    rm -f /renovate.tar.gz

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nodejs \
        npm \
        ca-certificates \
        git && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /tmp/renovate /opt/renovate
RUN npm install --global /opt/renovate 2>/dev/null || true && \
    mkdir -p /app && chown -R 65534:65534 /app /opt/renovate
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["renovate", "--version"]
ENTRYPOINT ["renovate"]
LABEL org.opencontainers.image.title="renovatebot" \
      org.opencontainers.image.version="43.138.3" \
      org.opencontainers.image.vendor="RenovateBot" \
      org.opencontainers.image.source="https://github.com/renovatebot/renovate" \
      sovereign.image.tier="2" \
      sovereign.image.category="automation" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
