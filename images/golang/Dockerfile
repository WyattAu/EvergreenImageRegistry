# =============================================================================
# SOVEREIGN HARDENED GOLANG
# Generated from template - Version: 1.22.3
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.22.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    golang-go ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin go 2>/dev/null || true
RUN mkdir -p /app /var/log/go /var/cache/go

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    golang-go ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove apt apt-get dpkg 2>/dev/null || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/go /var/log/go
COPY --from=builder --chown=65534:65534 /var/cache/go /var/cache/go
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD go version
ENTRYPOINT ["go"]
LABEL org.opencontainers.image.title="golang" \
      org.opencontainers.image.version="1.22.3" \
      org.opencontainers.image.vendor="Go" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.hardened="true"
