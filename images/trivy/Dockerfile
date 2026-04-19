# =============================================================================
# SOVEREIGN HARDENED TRIVY
# Generated from template - Version: 0.53.0
# Constraint: distroless/static - no shell, no package manager
# =============================================================================

ARG VERSION=0.53.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://github.com/aquasecurity/trivy/releases/download/v0.53.0/trivy_0.53.0_linux_amd64.tar.gz" -o /trivy.tar.gz && \
    tar -xzf /trivy.tar.gz -C / && rm /trivy.tar.gz && chmod +x /trivy

FROM cgr.dev/chainguard/wolfi AS builder
RUN mkdir -p /app /var/log/trivy /var/cache/trivy

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /trivy /trivy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/trivy /var/log/trivy
COPY --from=builder /var/cache/trivy /var/cache/trivy
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD trivy --version 2>/dev/null || exit 1
ENTRYPOINT ["/trivy"]
LABEL org.opencontainers.image.title="trivy" \
      org.opencontainers.image.version="0.53.0" \
      org.opencontainers.image.vendor="Aqua Security" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
