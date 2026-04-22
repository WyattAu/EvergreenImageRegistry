# =============================================================================
# SOVEREIGN HARDENED BLAZEBASE
# Constraint: debian-slim - niche database, placeholder binary
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: PLACEHOLDER - no upstream static binary available
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -s /usr/sbin/nologin blazebase 2>/dev/null || true
RUN mkdir -p /var/lib/blazebase /var/log/blazebase /var/cache/blazebase /app
RUN printf '#!/bin/sh\necho "blazebase v%s - placeholder (no upstream binary)"\nsleep infinity' "${VERSION}" > /app/blazebase && chmod +x /app/blazebase
RUN chown -R 65532:65532 /var/lib/blazebase /var/log/blazebase /var/cache/blazebase /app
USER 65532:65532
WORKDIR /app
EXPOSE 5432
ENTRYPOINT ["/app/blazebase"]
LABEL org.opencontainers.image.title="blazebase" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Blazebase - niche database (placeholder)" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="placeholder" \
      sovereign.image.note="No upstream binary available. Replace placeholder when upstream publishes releases." \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM