# =============================================================================
# SOVEREIGN HARDENED OPENVPN
# Generated from template - Version: 2.6.10
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=2.6.10
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "" -o /openvpn && chmod +x /openvpn 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
RUN adduser -D -u 65534 appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/openvpn /var/cache/openvpn
USER appuser
WORKDIR /app
COPY --from=downloader /openvpn /usr/local/bin/openvpn
EXPOSE 1194
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD openvpn openvpn --version
ENTRYPOINT ["/usr/local/bin/openvpn"]
LABEL org.opencontainers.image.title="openvpn" \
      org.opencontainers.image.version="2.6.10" \
      org.opencontainers.image.vendor="OpenVPN" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
