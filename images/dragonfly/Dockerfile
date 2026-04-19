# =============================================================================
# SOVEREIGN HARDENED DRAGONFLY
# Generated from template - Version: 1.21.0
# =============================================================================

ARG VERSION=1.21.0
ARG BUILD_DATE

FROM alpine:1.21.0-alpine
RUN apk add --no-cache dragonfly ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id dragonfly 2>/dev/null || adduser -D -u 65534 dragonfly
RUN mkdir -p /app /var/log/dragonfly /var/cache/dragonfly && chown -R dragonfly:dragonfly /app /var/log/dragonfly /var/cache/dragonfly
USER dragonfly:dragonfly
WORKDIR /app
EXPOSE 6379 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ADMIN ping
ENTRYPOINT ["dragonfly"]
LABEL org.opencontainers.image.title="dragonfly" \
      org.opencontainers.image.version="1.21.0" \
      org.opencontainers.image.vendor="DragonflyDB" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
