# =============================================================================
# SOVEREIGN HARDENED MATTERMOST
# Generated from template - Version: 11.6.0
# Constraint: wolfi - Chaenguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=11.6.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://releases.mattermost.com/${VERSION}/mattermost-team-${VERSION}-linux-amd64.tar.gz" -o /mattermost.tar.gz && \
    tar -xzf /mattermost.tar.gz -C / && rm /mattermost.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest
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
      org.opencontainers.image.version="11.6.0" \
      org.opencontainers.image.vendor="Mattermost" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
