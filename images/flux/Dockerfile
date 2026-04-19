# =============================================================================
# SOVEREIGN HARDENED FLUX
# Generated from template - Version: 2.3.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=2.3.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:2.3.0
RUN apk add --no-cache flux ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 flux 2>/dev/null || true
RUN mkdir -p /app /var/log/flux /var/cache/flux && chown -R flux:flux /app /var/log/flux /var/cache/flux 2>/dev/null || true
USER flux:flux
WORKDIR /app
EXPOSE 3030
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /./
ENTRYPOINT ["flux"]
LABEL org.opencontainers.image.title="flux" \
      org.opencontainers.image.version="2.3.0" \
      org.opencontainers.image.vendor="Flux" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
