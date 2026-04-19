# =============================================================================
# SOVEREIGN HARDENED COCKROACHDB
# Generated from template - Version: 23.2.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=23.2.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends cockroachdb ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' cockroach 2>/dev/null || true
RUN mkdir -p /app /var/log/cockroach /var/cache/cockroach && chown -R cockroach:cockroach /app /var/log/cockroach /var/cache/cockroach 2>/dev/null || true
USER cockroach
WORKDIR /app
EXPOSE 26257 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD cockroach sql --insecure -e "SELECT 1"
ENTRYPOINT ["cockroach"]
LABEL org.opencontainers.image.title="cockroachdb" \
      org.opencontainers.image.version="23.2.0" \
      org.opencontainers.image.vendor="CockroachDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
