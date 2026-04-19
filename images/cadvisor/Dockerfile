# =============================================================================
# SOVEREIGN HARDENED CADVISOR
# Generated from template - Version: 0.49.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=0.49.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:0.49.0
RUN apk add --no-cache cadvisor ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 cadv 2>/dev/null || true
RUN mkdir -p /app /var/log/cadvisor /var/cache/cadvisor && chown -R cadv:cadv /app /var/log/cadvisor /var/cache/cadvisor 2>/dev/null || true
USER cadv:cadv
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /healthz
ENTRYPOINT ["cadvisor"]
LABEL org.opencontainers.image.title="cadvisor" \
      org.opencontainers.image.version="0.49.0" \
      org.opencontainers.image.vendor="Google" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
