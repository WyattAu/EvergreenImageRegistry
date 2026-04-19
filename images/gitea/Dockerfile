# =============================================================================
# SOVEREIGN HARDENED GITEA
# Generated from template - Version: 1.21.0
# =============================================================================

ARG VERSION=1.21.0
ARG BUILD_DATE

FROM alpine:1.21.0-alpine
RUN apk add --no-cache gitea ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id git 2>/dev/null || adduser -D -u 65534 git
RUN mkdir -p /app /var/log/gitea /var/cache/gitea && chown -R git:git /app /var/log/gitea /var/cache/gitea
USER git:git
WORKDIR /app
EXPOSE 3000 22
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /api/health
ENTRYPOINT ["gitea"]
LABEL org.opencontainers.image.title="gitea" \
      org.opencontainers.image.version="1.21.0" \
      org.opencontainers.image.vendor="Gitea" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
