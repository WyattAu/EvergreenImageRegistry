# =============================================================================
# SOVEREIGN HARDENED ARGOCD
# Generated from template - Version: v2.14.0
# Constraint: official - ArgoCD is complex, use official base
# =============================================================================

ARG VERSION=v2.14.0
ARG BUILD_DATE

FROM argocd/argocd:${VERSION}

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65534 -g '' argocd 2>/dev/null || true && \
    chown -R argocd:argocd /home/argocd 2>/dev/null || true
USER argocd

WORKDIR /home/argocd
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -s localhost:8080/healthz || exit 1

LABEL org.opencontainers.image.title="argocd" \
      org.opencontainers.image.version="v2.14.0" \
      org.opencontainers.image.vendor="ArgoCD" \
      org.opencontainers.image.source="https://github.com/argoproj/argo-cd" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"