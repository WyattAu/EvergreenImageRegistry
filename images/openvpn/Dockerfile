# =============================================================================
# SOVEREIGN HARDENED OPENVPN
# Generated from template - Version: 2.6.10
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=2.6.10
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache openvpn 


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates 
RUN adduser -D -u 65532 appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/openvpn /var/cache/openvpn 2>/dev/null || true
USER appuser
WORKDIR /app
COPY --from=downloader /usr/sbin/openvpn /usr/local/bin/openvpn
EXPOSE 1194
ENTRYPOINT ["/usr/local/bin/openvpn"]
LABEL org.opencontainers.image.title="openvpn" \
      org.opencontainers.image.version="2.6.10" \
      org.opencontainers.image.vendor="OpenVPN" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM