# =============================================================================
# SOVEREIGN HARDENED ACTIVEMQ
# Generated from template - Version: 6.1.0
# =============================================================================

ARG VERSION=6.1.0
ARG BUILD_DATE

FROM alpine:6.1.0-alpine
RUN apk add --no-cache activemq ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id activemq 2>/dev/null || adduser -D -u 65534 activemq
RUN mkdir -p /app /var/log/activemq /var/cache/activemq && chown -R activemq:activemq /app /var/log/activemq /var/cache/activemq
USER activemq:activemq
WORKDIR /app
EXPOSE 61616 8161
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD activemq status
ENTRYPOINT ["activemq"]
LABEL org.opencontainers.image.title="activemq" \
      org.opencontainers.image.version="6.1.0" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
