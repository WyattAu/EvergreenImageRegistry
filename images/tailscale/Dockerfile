# =============================================================================
# SOVEREIGN HARDENED TAILSCALE
# Generated from template - Version: 1.66.1
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=1.66.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:20240415 AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "" -o /tailscale && chmod +x /tailscale 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:20240415
RUN adduser -D -u 65534 appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/tailscale /var/cache/tailscale
USER appuser
WORKDIR /app
COPY --from=downloader /tailscale /usr/local/bin/tailscale
EXPOSE 41641
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /usr/local/bin/tailscale status
ENTRYPOINT ["/usr/local/bin/tailscale"]
LABEL org.opencontainers.image.title="tailscale" \
      org.opencontainers.image.version="1.66.1" \
      org.opencontainers.image.vendor="Tailscale" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
