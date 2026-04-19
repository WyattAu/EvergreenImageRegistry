# =============================================================================
# SOVEREIGN HARDENED VAULTWARDEN
# Generated from template - Version: 2026.4.1
# =============================================================================

ARG VERSION=2026.4.1
ARG BUILD_DATE

FROM alpine:2026.4.1-alpine
RUN apk add --no-cache vaultwarden ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id vaultwarden 2>/dev/null || adduser -D -u 65534 vaultwarden
RUN mkdir -p /app /var/log/vaultwarden /var/cache/vaultwarden && chown -R vaultwarden:vaultwarden /app /var/log/vaultwarden /var/cache/vaultwarden
USER vaultwarden:vaultwarden
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /alive
ENTRYPOINT ["vaultwarden"]
LABEL org.opencontainers.image.title="vaultwarden" \
      org.opencontainers.image.version="2026.4.1" \
      org.opencontainers.image.vendor="Vaultwarden" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
