# =============================================================================
# SOVEREIGN HARDENED LDAPBROWSER
# Apache Directory Studio LDAP browser - Java app
# Constraint: debian-slim + JRE - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.0.0.v20230628M17
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/ltiam/APacheDirectoryStudio/releases/download/${VERSION}/ApacheDirectoryStudio-${VERSION}-linux.gtk.x86_64.tar.gz" -o /studio.tar.gz && \
    mkdir -p /tmp/studio && \
    tar -xzf /studio.tar.gz -C /tmp/studio --strip-components=1 && \
    rm -f /studio.tar.gz

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless \
        libgtk-3-0 \
        libswt-gtk-4-java \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /tmp/studio /opt/ApacheDirectoryStudio
RUN mkdir -p /app && chown -R 65534:65534 /app /opt/ApacheDirectoryStudio
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/opt/ApacheDirectoryStudio/ApacheDirectoryStudio", "--help"]
ENTRYPOINT ["/opt/ApacheDirectoryStudio/ApacheDirectoryStudio"]
LABEL org.opencontainers.image.title="ldapbrowser" \
      org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.source="https://github.com/ltiam/APacheDirectoryStudio" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="15000ms"
