# =============================================================================
# SOVEREIGN HARDENED CADVISOR
# Generated from template - Version: 0.49.1
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=0.49.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "" -o /cadvisor && chmod +x /cadvisor 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
RUN adduser -D -u 65534 appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/cadvisor /var/cache/cadvisor
USER appuser
WORKDIR /app
COPY --from=downloader /cadvisor /usr/local/bin/cadvisor
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD cadvisor cadvisor --version
ENTRYPOINT ["/usr/local/bin/cadvisor"]
LABEL org.opencontainers.image.title="cadvisor" \
      org.opencontainers.image.version="0.49.1" \
      org.opencontainers.image.vendor="Google" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
