# =============================================================================
# SOVEREIGN HARDENED TRIVY
# Generated from template - Version: 0.53.0
# =============================================================================

ARG VERSION=0.53.0
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://github.com/aquasecurity/trivy/releases/download/v0.53.0/trivy_0.53.0_linux_amd64.tar.gz" -o /trivy.tar.gz && \
    tar -xzf /trivy.tar.gz -C / && rm /trivy.tar.gz && chmod +x /trivy

FROM scratch
COPY --from=downloader /trivy /trivy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /trivy && chmod +x /trivy
RUN mkdir -p /app /var/log/trivy /var/cache/trivy && chown 65534:65534 /app /var/log/trivy /var/cache/trivy
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:8080/trivy --version || exit 1
ENTRYPOINT ["/trivy"]
LABEL org.opencontainers.image.title="trivy" \
      org.opencontainers.image.version="0.53.0" \
      org.opencontainers.image.vendor="Aqua Security" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
