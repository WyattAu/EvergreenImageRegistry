# =============================================================================
# SOVEREIGN HARDENED ARGOCD
# Generated from template - Version: 2.13.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=2.13.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends argocd ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' argocd 2>/dev/null || true
RUN mkdir -p /app /var/log/argocd /var/cache/argocd && chown -R argocd:argocd /app /var/log/argocd /var/cache/argocd 2>/dev/null || true
USER argocd:argocd
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /healthz
ENTRYPOINT ["argocd"]
LABEL org.opencontainers.image.title="argocd" \
      org.opencontainers.image.version="2.13.0" \
      org.opencontainers.image.vendor="ArgoCD" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
