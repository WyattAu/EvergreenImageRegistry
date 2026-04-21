# =============================================================================
# SOVEREIGN HARDENED WG-QUICK
# Generated from template - Version: 1.0.20210914
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=1.0.20210914
ARG BUILD_DATE

# hadolint ignore=DL3007
FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
# hadolint ignore=DL3018
RUN apk add --no-cache wireguard-tools

# hadolint ignore=DL3007
FROM cgr.dev/chainguard/wolfi-base:latest
RUN adduser -D -u 65534 appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/wg /var/cache/wg
USER appuser
WORKDIR /app
# hadolint ignore=DL3021
COPY --from=downloader /usr/bin/wg /usr/local/bin/wg
# hadolint ignore=DL3021
COPY --from=downloader /usr/bin/wg-quick /usr/local/bin/wg-quick 2>/dev/null || true
EXPOSE 51820
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /usr/local/bin/wg show
ENTRYPOINT ["/usr/local/bin/wg"]
LABEL org.opencontainers.image.title="wg-quick" \
      org.opencontainers.image.version="1.0.20210914" \
      org.opencontainers.image.vendor="WireGuard" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
