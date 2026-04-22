# =============================================================================
# SOVEREIGN HARDENED TOOLJET
# Generated from template - Version: 2.57.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.57.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm ca-certificates curl && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 65534 -s /usr/sbin/nologin app 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove apt-get dpkg 2>/dev/null || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/node /var/log/node
COPY --from=builder --chown=65534:65534 /var/cache/node /var/cache/node
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8080/api/v1/health
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="tooljet" \
      org.opencontainers.image.version="2.57.0" \
      org.opencontainers.image.vendor="ToolJet/ToolJet" \
      org.opencontainers.image.source="https://github.com/ToolJet/ToolJet/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.hardened="true"
