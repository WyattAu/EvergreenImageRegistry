# =============================================================================
# SOVEREIGN HARDENED WG-QUICK
# Generated from template - Version: 1.0.20210914
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=1.0.20210914
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "" -o /wg && chmod +x /wg 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
RUN adduser -D -u 65534 appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/wg /var/cache/wg
USER appuser
WORKDIR /app
COPY --from=downloader /wg /usr/local/bin/wg
EXPOSE 51820
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wg wg show
ENTRYPOINT ["/usr/local/bin/wg"]
LABEL org.opencontainers.image.title="wg-quick" \
      org.opencontainers.image.version="1.0.20210914" \
      org.opencontainers.image.vendor="WireGuard" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
