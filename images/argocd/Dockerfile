# =============================================================================
# SOVEREIGN HARDENED ARGOCD
# Generated from template - Version: 2.13.0
# =============================================================================

ARG VERSION=2.13.0
ARG BUILD_DATE

FROM alpine:2.13.0-alpine
RUN apk add --no-cache argocd ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id argocd 2>/dev/null || adduser -D -u 65534 argocd
RUN mkdir -p /app /var/log/argocd /var/cache/argocd && chown -R argocd:argocd /app /var/log/argocd /var/cache/argocd
USER argocd:argocd
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /healthz
ENTRYPOINT ["argocd"]
LABEL org.opencontainers.image.title="argocd" \
      org.opencontainers.image.version="2.13.0" \
      org.opencontainers.image.vendor="ArgoCD" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
