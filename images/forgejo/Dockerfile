# =============================================================================
# SOVEREIGN HARDENED FORGEJO
# Generated from template - Version: 1.21.11
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=1.21.11
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://codeberg.org/forgejo/forgejo/releases/download/1.21.11/forgejo-1.21.11-linux-amd64" -o /forgejo && chmod +x /forgejo 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
RUN adduser -D -u 65534 git 2>/dev/null || true
RUN mkdir -p /app /var/log/forgejo /var/cache/forgejo
USER git
WORKDIR /app
COPY --from=downloader /forgejo /usr/local/bin/forgejo
EXPOSE 3000 22
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD forgejo forgejo --version
ENTRYPOINT ["/usr/local/bin/forgejo"]
LABEL org.opencontainers.image.title="forgejo" \
      org.opencontainers.image.version="1.21.11" \
      org.opencontainers.image.vendor="Forgejo" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
