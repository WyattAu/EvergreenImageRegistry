# =============================================================================
# SOVEREIGN HARDENED SUBSONIC
# Generated from template - Version: 6.17.1
# Constraint: debian-slim - JRE required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=6.17.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/subsonic/subsonic/releases/download/v6.17.1/subsonic-6.17.1.jar" -o /app/subsonic-6.17.1.jar

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre-headless ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
COPY --from=downloader --chown=65534:65534 /app /app
RUN mkdir -p /var/log/subsonic /var/cache/subsonic && chown -R 65534:65534 /var/log/subsonic /var/cache/subsonic 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 4040
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -sf http://localhost:4040/ || exit 1
ENTRYPOINT ["java", "-jar", "/app/subsonic-6.17.1.jar"]
LABEL org.opencontainers.image.title="subsonic" \
      org.opencontainers.image.version="6.17.1" \
      org.opencontainers.image.vendor="Subsonic" \
      org.opencontainers.image.source="https://github.com/subsonic/subsonic/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
