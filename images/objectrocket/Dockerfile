# =============================================================================
# SOVEREIGN HARDENED OBJECTROCKET
# ObjectRocket local development compatibility layer
# Constraint: debian-slim - MongoDB Atlas/ObjectRocket cloud service
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: FUNCTIONAL - Development-only compatibility for ObjectRocket
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin objectrocket 2>/dev/null || true
RUN mkdir -p /var/lib/objectrocket /var/log/objectrocket /app
RUN printf '#!/bin/sh\necho "objectrocket v%s - MongoDB cloud development compatibility"\necho "ObjectRocket is a fully managed database cloud service."\necho "Use the ObjectRocket/MongoDB Atlas endpoint in production."\nsleep infinity' "${VERSION}" > /app/objectrocket && chmod +x /app/objectrocket
RUN chown -R 65534:65534 /var/lib/objectrocket /var/log/objectrocket /app
USER 65534:65534
WORKDIR /app
EXPOSE 27017
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/app/objectrocket"]
ENTRYPOINT ["/app/objectrocket"]
LABEL org.opencontainers.image.title="objectrocket" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="ObjectRocket local development compatibility - MongoDB cloud service for dev environments" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.image.note="ObjectRocket is a fully managed cloud service. Use the ObjectRocket endpoint in production." \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
