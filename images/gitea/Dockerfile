# =============================================================================
# SOVEREIGN HARDENED GITEA
# Generated from template - Version: 1.21.10
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=1.21.10
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://github.com/go-gitea/gitea/releases/download/v1.21.10/gitea-1.21.10-linux-amd64" -o /gitea && chmod +x /gitea 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
RUN adduser -D -u 65534 git 2>/dev/null || true
RUN mkdir -p /app /var/log/gitea /var/cache/gitea
USER git
WORKDIR /app
COPY --from=downloader /gitea /usr/local/bin/gitea
EXPOSE 3000 22
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD gitea gitea --version
ENTRYPOINT ["/usr/local/bin/gitea"]
LABEL org.opencontainers.image.title="gitea" \
      org.opencontainers.image.version="1.21.10" \
      org.opencontainers.image.vendor="Gitea" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
