# =============================================================================
# SOVEREIGN HARDENED MODSECURITY
# Generated from template - Version: 2.4.59
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.4.59
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends apache2 libapache2-mod-security2 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/apache2 /var/cache/apache2 && chown -R appuser:appuser /app /var/log/apache2 /var/cache/apache2 2>/dev/null || true
USER appuser
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /usr/sbin/apache2 -v
ENTRYPOINT ["apache2"]
LABEL org.opencontainers.image.title="modsecurity" \
      org.opencontainers.image.version="2.4.59" \
      org.opencontainers.image.vendor="OWASP" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
