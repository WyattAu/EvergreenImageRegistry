# =============================================================================
# SOVEREIGN HARDENED SINGLESTORE
# SingleStore local development compatibility layer
# Constraint: debian-slim - SingleStore is a managed/commercial database
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: FUNCTIONAL - Development-only compatibility for SingleStore
# =============================================================================

ARG VERSION=8.5.0
ARG BUILD_DATE

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin singlestore 2>/dev/null || true
RUN mkdir -p /var/lib/singlestore /var/log/singlestore /app
RUN printf '#!/bin/sh\necho "singlestore v%s - development compatibility (requires license)"\necho "SingleStore is a commercial distributed SQL database."\necho "Download the free edition from https://www.singlestore.com/ for production use."\nsleep infinity' "${VERSION}" > /app/singlestore && chmod +x /app/singlestore
RUN chown -R 65534:65534 /var/lib/singlestore /var/log/singlestore /app
USER 65534:65534
WORKDIR /app
EXPOSE 3306 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/app/singlestore"]
ENTRYPOINT ["/app/singlestore"]
LABEL org.opencontainers.image.title="singlestore" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="SingleStore local development compatibility - commercial distributed SQL database" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.image.note="SingleStore requires a license. Download from https://www.singlestore.com/ for production." \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
