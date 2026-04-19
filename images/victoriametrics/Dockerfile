# =============================================================================
# SOVEREIGN HARDENED VICTORIAMETRICS
# Generated from template - Version: 1.103.0
# =============================================================================

ARG VERSION=1.103.0
ARG BUILD_DATE

FROM alpine:1.103.0-alpine
RUN apk add --no-cache victoria-metrics ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id victoria 2>/dev/null || adduser -D -u 65534 victoria
RUN mkdir -p /app /var/log/victoriametrics /var/cache/victoriametrics && chown -R victoria:victoria /app /var/log/victoriametrics /var/cache/victoriametrics
USER victoria:victoria
WORKDIR /app
EXPOSE 8428
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /health
ENTRYPOINT ["victoria-metrics"]
LABEL org.opencontainers.image.title="victoriametrics" \
      org.opencontainers.image.version="1.103.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
