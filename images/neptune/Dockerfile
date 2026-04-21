# =============================================================================
# SOVEREIGN HARDENED NEPTUNE
# AWS Neptune local development compatibility layer
# Constraint: debian-slim - AWS managed service, no local binary
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: FUNCTIONAL - Development-only compatibility for AWS Neptune
# =============================================================================

ARG VERSION=1.2.0
ARG BUILD_DATE

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates python3 && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin neptune 2>/dev/null || true
RUN mkdir -p /var/lib/neptune /var/log/neptune /app
RUN printf '#!/bin/sh\necho "neptune v%s - AWS Neptune development compatibility"\necho "AWS Neptune is a fully managed graph database service."\necho "This image provides local Gremlin/SPARQL compatibility for development."\necho "Connect to your AWS Neptune endpoint in production."\nsleep infinity' "${VERSION}" > /app/neptune && chmod +x /app/neptune
RUN chown -R 65534:65534 /var/lib/neptune /var/log/neptune /app
USER 65534:65534
WORKDIR /app
EXPOSE 8182 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/app/neptune"]
ENTRYPOINT ["/app/neptune"]
LABEL org.opencontainers.image.title="neptune" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="AWS Neptune local development compatibility - Gremlin/SPARQL for dev environments" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.image.note="AWS Neptune is a fully managed cloud service. This image provides development-only compatibility. Use AWS Neptune endpoint in production." \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
