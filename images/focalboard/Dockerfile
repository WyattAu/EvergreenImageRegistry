# =============================================================================
# SOVEREIGN HARDENED FOCALBOARD
# ARCHIVED: Focalboard has been merged into Mattermost as a plugin (Boards).
# This image is maintained as a stub. For active use, install the
# mattermost-plugin-focalboard plugin into a Mattermost server.
# See: https://github.com/mattermost/focalboard
# =============================================================================

ARG VERSION=8.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/mattermost/focalboard/releases/download/v${VERSION}/mattermost-plugin-focalboard-v${VERSION}-linux-amd64.tar.gz" -o /focalboard.tar.gz && \
    tar -xzf /focalboard.tar.gz -C /opt && rm /focalboard.tar.gz

FROM debian:bookworm-slim
RUN useradd -m -u 65534 -g '' focalboard 2>/dev/null || true
RUN mkdir -p /app /var/log/focalboard /var/cache/focalboard
COPY --from=downloader /opt /app/plugins
USER focalboard
WORKDIR /app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD test -d /app/plugins || exit 1
ENTRYPOINT ["echo", "Focalboard is now a Mattermost plugin. See https://github.com/mattermost/focalboard"]
LABEL org.opencontainers.image.title="focalboard" \
      org.opencontainers.image.version="8.0.0" \
      org.opencontainers.image.vendor="Mattermost" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.image.archived="true" \
      sovereign.image.replacement="mattermost"
