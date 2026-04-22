# =============================================================================
# SOVEREIGN HARDENED SQLITE
# Generated from template - Version: 3.45.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.45.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends sqlite-libs ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -g '' sqlite 2>/dev/null || true
RUN mkdir -p /app /var/log/sqlite-libs /var/cache/sqlite-libs && chown -R sqlite:sqlite /app /var/log/sqlite-libs /var/cache/sqlite-libs 2>/dev/null || true
USER sqlite
WORKDIR /app
ENTRYPOINT ["sqlite-libs"]
LABEL org.opencontainers.image.title="sqlite" \
      org.opencontainers.image.version="3.45.1" \
      org.opencontainers.image.vendor="SQLite" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM