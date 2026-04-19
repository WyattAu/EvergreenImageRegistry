# =============================================================================
# SOVEREIGN HARDENED STRONGSWAN
# Generated from template - Version: 6.0.1
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=6.0.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:20240415 AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "" -o /charon && chmod +x /charon 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:20240415
RUN adduser -D -u 65534 appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/charon /var/cache/charon
USER appuser
WORKDIR /app
COPY --from=downloader /charon /usr/local/bin/charon
EXPOSE 500 4500
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /usr/local/bin/ipsec status
ENTRYPOINT ["/usr/local/bin/charon"]
LABEL org.opencontainers.image.title="strongswan" \
      org.opencontainers.image.version="6.0.1" \
      org.opencontainers.image.vendor="StrongSwan" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
