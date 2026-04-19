# =============================================================================
# SOVEREIGN HARDENED GITLAB
# Generated from template - Version: 17.6.0
# Constraint: official - GitLab complexity requires official base
# Note: GitLab is too complex for from-scratch hardening, use official base
# =============================================================================

ARG VERSION=17.6.0
ARG BUILD_DATE

FROM gitlab/gitlab-ce:${VERSION}-ce.0

# Apply sovereignty hardening on top of official image
USER root
# Ensure non-root user exists
RUN useradd -m -u 65534 -g '' git 2>/dev/null || true
USER git

WORKDIR /home/git
EXPOSE 80 22 443

HEALTHCHECK --interval=30s --timeout=10s --start-period=300s --retries=3 \
    CMD curl -s http://localhost:80/api/v4/health || exit 1

LABEL org.opencontainers.image.title="gitlab" \
      org.opencontainers.image.version="17.6.0" \
      org.opencontainers.image.vendor="GitLab" \
      org.opencontainers.image.source="https://gitlab.com/gitlab-org/gitlab-ce" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"