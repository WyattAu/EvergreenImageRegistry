# =============================================================================
# SOVEREIGN HARDENED ZITADEL
# Generated from template - Version: 2.45.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=2.45.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends zitadel ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' zitadel 2>/dev/null || true
RUN mkdir -p /app /var/log/zitadel /var/cache/zitadel && chown -R zitadel:zitadel /app /var/log/zitadel /var/cache/zitadel 2>/dev/null || true
USER zitadel:zitadel
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /health
ENTRYPOINT ["zitadel"]
LABEL org.opencontainers.image.title="zitadel" \
      org.opencontainers.image.version="2.45.0" \
      org.opencontainers.image.vendor="Zitadel" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
