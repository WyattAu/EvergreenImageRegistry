# =============================================================================
# SOVEREIGN HARDENED NODE
# Generated from template - Version: 20.12.2
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=20.12.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin node 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove apt apt-get dpkg 2>/dev/null || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/node /var/log/node
COPY --from=builder --chown=65534:65534 /var/cache/node /var/cache/node
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node --version
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="node" \
      org.opencontainers.image.version="20.12.2" \
      org.opencontainers.image.vendor="Node.js" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.hardened="true"
