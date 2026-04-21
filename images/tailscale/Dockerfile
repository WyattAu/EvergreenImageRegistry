# =============================================================================
# SOVEREIGN HARDENED TAILSCALE
# Generated from template - Version: 1.66.1
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=1.66.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL -k "https://pkgs.tailscale.com/stable/tailscale_${VERSION}_linux_amd64.tgz" -o /tmp/tailscale.tgz && \
    tar -xzf /tmp/tailscale.tgz -C /tmp && \
    cp /tmp/tailscale_${VERSION}_linux_amd64/tailscale /tailscale && \
    cp /tmp/tailscale_${VERSION}_linux_amd64/tailscaled /tailscaled && \
    chmod +x /tailscale /tailscaled && \
    rm -rf /tmp/tailscale.tgz /tmp/tailscale_${VERSION}_linux_amd64

FROM cgr.dev/chainguard/wolfi-base:latest
RUN adduser -D -u 65534 appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/tailscale /var/cache/tailscale
USER appuser
WORKDIR /app
COPY --from=downloader /tailscale /usr/local/bin/tailscale
COPY --from=downloader /tailscaled /usr/local/bin/tailscaled
EXPOSE 41641
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /usr/local/bin/tailscale version
ENTRYPOINT ["/usr/local/bin/tailscaled"]
LABEL org.opencontainers.image.title="tailscale" \
      org.opencontainers.image.version="1.66.1" \
      org.opencontainers.image.vendor="Tailscale" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
