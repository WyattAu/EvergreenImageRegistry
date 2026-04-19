# =============================================================================
# SOVEREIGN HARDENED TEKTON
# Generated from template - Version: 0.61.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=0.61.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:0.61.0
RUN apk add --no-cache tekton ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 tekton 2>/dev/null || true
RUN mkdir -p /app /var/log/tekton /var/cache/tekton && chown -R tekton:tekton /app /var/log/tekton /var/cache/tekton 2>/dev/null || true
USER tekton:tekton
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /health
ENTRYPOINT ["tekton"]
LABEL org.opencontainers.image.title="tekton" \
      org.opencontainers.image.version="0.61.0" \
      org.opencontainers.image.vendor="Tekton" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
