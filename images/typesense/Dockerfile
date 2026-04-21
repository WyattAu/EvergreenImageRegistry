# =============================================================================
# SOVEREIGN HARDENED TYPESENSE
# Generated from template - Version: 30.2
# Constraint: debian-slim - binary download from Typesense
# =============================================================================

ARG VERSION=30.2
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    curl -fsSL -k "https://dl.typesense.org/releases/typesense-server-${VERSION}-amd64.deb" -o /tmp/typesense.deb && \
    dpkg -i /tmp/typesense.deb && \
    apt-get install -f -y && \
    rm -f /tmp/typesense.deb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/typesense /var/cache/typesense /var/lib/typesense
USER 65534:65534
WORKDIR /app
EXPOSE 8108
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["typesense-server", "--version"]
ENTRYPOINT ["typesense-server"]
LABEL org.opencontainers.image.title="typesense" \
      org.opencontainers.image.version="30.2" \
      org.opencontainers.image.vendor="Typesense" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
