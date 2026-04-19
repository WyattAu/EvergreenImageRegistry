# =============================================================================
# SOVEREIGN HARDENED GITLAB
# Generated from template - Version: 16.12.0
# =============================================================================

ARG VERSION=16.12.0
ARG BUILD_DATE

FROM alpine:16.12.0-alpine
RUN apk add --no-cache gitlab-ce ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id git 2>/dev/null || adduser -D -u 65534 git
RUN mkdir -p /app /var/log/gitlab /var/cache/gitlab && chown -R git:git /app /var/log/gitlab /var/cache/gitlab
USER git:git
WORKDIR /app
EXPOSE 80 22 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /api/v4/health
ENTRYPOINT ["gitlab-ce"]
LABEL org.opencontainers.image.title="gitlab" \
      org.opencontainers.image.version="16.12.0" \
      org.opencontainers.image.vendor="GitLab" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
