# =============================================================================
# SOVEREIGN HARDENED ZITADEL
# Generated from template - Version: 2.45.0
# =============================================================================

ARG VERSION=2.45.0
ARG BUILD_DATE

FROM alpine:2.45.0-alpine
RUN apk add --no-cache zitadel ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id zitadel 2>/dev/null || adduser -D -u 65534 zitadel
RUN mkdir -p /app /var/log/zitadel /var/cache/zitadel && chown -R zitadel:zitadel /app /var/log/zitadel /var/cache/zitadel
USER zitadel:zitadel
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /health
ENTRYPOINT ["zitadel"]
LABEL org.opencontainers.image.title="zitadel" \
      org.opencontainers.image.version="2.45.0" \
      org.opencontainers.image.vendor="Zitadel" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
