# =============================================================================
# SOVEREIGN HARDENED AIRSONIC-ADVANCED
# Generated from template - Version: 11.1.5
# Constraint: debian-slim - JRE required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=11.1.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/airsonic-advanced/airsonic-advanced/releases/download/v11.1.5/airsonic-advanced-11.1.5.war" -o /app/airsonic-advanced-11.1.5.war

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre-headless ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
COPY --from=downloader --chown=65534:65534 /app /app
RUN mkdir -p /var/log/airsonic-advanced /var/cache/airsonic-advanced && chown -R 65534:65534 /var/log/airsonic-advanced /var/cache/airsonic-advanced 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 4040
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -sf http://localhost:4040/ || exit 1
ENTRYPOINT ["java", "-jar", "/app/airsonic-advanced-11.1.5.war"]
LABEL org.opencontainers.image.title="airsonic-advanced" \
      org.opencontainers.image.version="11.1.5" \
      org.opencontainers.image.vendor="Airsonic-Advanced" \
      org.opencontainers.image.source="https://github.com/airsonic-advanced/airsonic-advanced/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
