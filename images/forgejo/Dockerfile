# =============================================================================
# SOVEREIGN HARDENED FORGEJO
# Generated from template - Version: 1.0.0
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM alpine:1.0.0-alpine
RUN apk add --no-cache forgejo ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id git 2>/dev/null || adduser -D -u 65534 git
RUN mkdir -p /app /var/log/forgejo /var/cache/forgejo && chown -R git:git /app /var/log/forgejo /var/cache/forgejo
USER git:git
WORKDIR /app
EXPOSE 3000 22
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /api/health
ENTRYPOINT ["forgejo"]
LABEL org.opencontainers.image.title="forgejo" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="Forgejo" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
