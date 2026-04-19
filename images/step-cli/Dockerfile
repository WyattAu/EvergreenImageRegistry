# =============================================================================
# SOVEREIGN HARDENED STEP-CLI
# Generated from template - Version: 0.25.2
# Constraint: distroless/static - no shell, no package manager
# =============================================================================

ARG VERSION=0.25.2
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://github.com/smallstep/cli/releases/download/v0.25.2/step_{_VERSION}_linux_amd64.tar.gz" -o /step.tar.gz && \
    tar -xzf /step.tar.gz -C / && rm /step.tar.gz && chmod +x /step

FROM cgr.dev/chainguard/wolfi AS builder
RUN mkdir -p /app /var/log/step /var/cache/step

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /step /step
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/step /var/log/step
COPY --from=builder /var/cache/step /var/cache/step
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD step --version 2>/dev/null || exit 1
ENTRYPOINT ["/step"]
LABEL org.opencontainers.image.title="step-cli" \
      org.opencontainers.image.version="0.25.2" \
      org.opencontainers.image.vendor="Smallstep" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
