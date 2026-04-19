# =============================================================================
# SOVEREIGN HARDENED UNBOUND
# Generated from template - Version: 1.20.0
# Constraint: distroless/static - no shell, no package manager
# =============================================================================

ARG VERSION=1.20.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://unbound.net/" -o /unbound.tar.gz && \
    tar -xzf /unbound.tar.gz -C / && rm /unbound.tar.gz && chmod +x /unbound

FROM cgr.dev/chainguard/wolfi AS builder
RUN mkdir -p /app /var/log/unbound /var/cache/unbound

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /unbound /unbound
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/unbound /var/log/unbound
COPY --from=builder /var/cache/unbound /var/cache/unbound
USER 65534:65534
WORKDIR /app
EXPOSE 53
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD unbound --version 2>/dev/null || exit 1
ENTRYPOINT ["/unbound"]
LABEL org.opencontainers.image.title="unbound" \
      org.opencontainers.image.version="1.20.0" \
      org.opencontainers.image.vendor="NLnet Labs" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
