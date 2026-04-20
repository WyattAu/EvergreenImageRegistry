# =============================================================================
# SOVEREIGN HARDENED NETCLIENT
# Generated from template - Version: 0.24.0
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=0.24.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "" -o /netclient && chmod +x /netclient 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
RUN adduser -D -u 65534 appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/netclient /var/cache/netclient
USER appuser
WORKDIR /app
COPY --from=downloader /netclient /usr/local/bin/netclient
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /usr/local/bin/netclient --version
ENTRYPOINT ["/usr/local/bin/netclient"]
LABEL org.opencontainers.image.title="netclient" \
      org.opencontainers.image.version="0.24.0" \
      org.opencontainers.image.vendor="NetMaker" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
