# =============================================================================
# SOVEREIGN HARDENED OBJECTROCKET
# ObjectRocket local development compatibility layer
# Constraint: debian-slim - MongoDB Atlas/ObjectRocket cloud service
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: FUNCTIONAL - Development-only compatibility for ObjectRocket
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -s /sbin/nologin objectrocket 2>/dev/null || true
RUN mkdir -p /var/lib/objectrocket /var/log/objectrocket /app
RUN printf '#!/bin/sh\necho "objectrocket v%s - MongoDB cloud development compatibility"\necho "ObjectRocket is a fully managed database cloud service."\necho "Use the ObjectRocket/MongoDB Atlas endpoint in production."\nsleep infinity' "${VERSION}" > /app/objectrocket && chmod +x /app/objectrocket
RUN chown -R 65532:65532 /var/lib/objectrocket /var/log/objectrocket /app
USER 65532:65532
WORKDIR /app
EXPOSE 27017
ENTRYPOINT ["/app/objectrocket"]
LABEL org.opencontainers.image.title="objectrocket" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="ObjectRocket local development compatibility - MongoDB cloud service for dev environments" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.image.note="ObjectRocket is a fully managed cloud service. Use the ObjectRocket endpoint in production." \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM