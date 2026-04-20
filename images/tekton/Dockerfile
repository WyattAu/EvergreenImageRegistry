# =============================================================================
# SOVEREIGN HARDENED TEKTON
# Generated from template - Version: latest
# Constraint: official - Tekton is complex, use official base
# =============================================================================

ARG VERSION=latest
ARG BUILD_DATE

FROM ghcr.io/tektoncd/cli:${VERSION}

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65534 -g '' tekton 2>/dev/null || true && \
    chown -R tekton:tekton /home/tekton 2>/dev/null || true
USER tekton

WORKDIR /home/tekton

LABEL org.opencontainers.image.title="tekton" \
      org.opencontainers.image.version="latest" \
      org.opencontainers.image.vendor="Tekton" \
      org.opencontainers.image.source="https://github.com/tektoncd/cli" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"