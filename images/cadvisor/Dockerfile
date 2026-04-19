# =============================================================================
# SOVEREIGN HARDENED CADVISOR
# Generated from template - Version: 0.49.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=0.49.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends cadvisor ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' cadv 2>/dev/null || true
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
      sovereign.constraint.debian_slim="true"
