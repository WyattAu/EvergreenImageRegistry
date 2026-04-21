# =============================================================================
# SOVEREIGN HARDENED HOMEPAGE
# Generated from template - Version: 1.12.3
# Constraint: debian-slim - no prebuilt binaries; built from source
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.12.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/nodesource/distributions/setup_20.x" | bash - && \
    apt-get install -y --no-install-recommends nodejs && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v${VERSION} https://github.com/gethomepage/homepage.git /tmp/homepage && \
    cd /tmp/homepage && npm ci && npm run build && \
    mkdir -p /app && cp -r dist/* /app/ && rm -rf /tmp/homepage

FROM debian:bookworm-slim AS runner
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' homepage 2>/dev/null || true
RUN mkdir -p /app /var/log/homepage /var/cache/homepage && chown -R homepage:homepage /app /var/log/homepage /var/cache/homepage 2>/dev/null || true
COPY --from=builder /app /app
USER homepage
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:3000/api/health || exit 1
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="homepage" \
      org.opencontainers.image.version="1.12.3" \
      org.opencontainers.image.vendor="Homepage" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
