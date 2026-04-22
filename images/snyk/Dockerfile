# =============================================================================
# SOVEREIGN HARDENED SNYK
# Security vulnerability scanner - Node.js app
# Constraint: debian-slim + Node.js - Node runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.1300.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/snyk/snyk/releases/download/v${VERSION}/snyk-linux" -o /snyk && \
    chmod +x /snyk && \
    strip --strip-all /snyk

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nodejs \
        npm \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /snyk /usr/local/bin/snyk
RUN mkdir -p /app && chown 65534:65534 /app
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/snyk", "--version"]
ENTRYPOINT ["/usr/local/bin/snyk"]
LABEL org.opencontainers.image.title="snyk" \
      org.opencontainers.image.version="1.1300.0" \
      org.opencontainers.image.vendor="Snyk" \
      org.opencontainers.image.source="https://github.com/snyk/snyk" \
      sovereign.image.tier="2" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
