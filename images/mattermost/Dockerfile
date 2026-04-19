# =============================================================================
# SOVEREIGN HARDENED MATTERMOST
# Generated from template - Version: 10.11.14
# Constraint: wolfi - Chaenguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=10.11.14
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:20240415 AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://github.com/mattermost/mattermost/releases/download/v${VERSION}/mattermost-${VERSION}-linux-amd64.tar.gz" -o /mattermost.tar.gz && \
    tar -xzf /mattermost.tar.gz -C / && rm /mattermost.tar.gz

FROM cgr.dev/chainguard/wolfi-base:20240415
RUN addgroup -g 65534 mattermost || true
RUN adduser -D -u 65534 -G mattermost mattermost || true
RUN mkdir -p /app /var/log/mattermost /var/cache/mattermost
COPY --from=downloader /mattermost /app/mattermost
USER mattermost
WORKDIR /app
EXPOSE 8065
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/bin/curl", "-sf", "http://localhost:8065/api/v4/system/ping"]
ENTRYPOINT ["/app/mattermost/bin/mattermost"]
LABEL org.opencontainers.image.title="mattermost" \
      org.opencontainers.image.version="10.11.14" \
      org.opencontainers.image.vendor="Mattermost" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"