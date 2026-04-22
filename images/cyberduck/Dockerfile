# =============================================================================
# SOVEREIGN HARDENED CYBERDUCK
# Multi-protocol file transfer client - Java app
# Constraint: debian-slim + JRE - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=9.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/iterate-ch/cyberduck/releases/download/${VERSION}/Cyberduck-${VERSION}.tar.gz" -o /cyberduck.tar.gz && \
    mkdir -p /tmp/cyberduck && \
    tar -xzf /cyberduck.tar.gz -C /tmp/cyberduck && \
    rm -f /cyberduck.tar.gz

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless \
        libswt-gtk-4-java \
        libgtk-3-0 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /tmp/cyberduck /opt/cyberduck
RUN mkdir -p /app && chown -R 65534:65534 /app /opt/cyberduck
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/opt/cyberduck/Cyberduck", "--help"]
ENTRYPOINT ["/opt/cyberduck/Cyberduck"]
LABEL org.opencontainers.image.title="cyberduck" \
      org.opencontainers.image.version="9.1.0" \
      org.opencontainers.image.vendor="iterate-ch" \
      org.opencontainers.image.source="https://github.com/iterate-ch/cyberduck" \
      sovereign.image.tier="2" \
      sovereign.image.category="storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="15000ms"
