# =============================================================================
# SOVEREIGN HARDENED COSIGN
# Generated from template - Version: 2.4.0
# =============================================================================

ARG VERSION=2.4.0
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://github.com/sigstore/cosign/releases/download/v2.4.0/cosign_2.4.0_linux_amd64" -o /cosign.tar.gz && \
    tar -xzf /cosign.tar.gz -C / && rm /cosign.tar.gz && chmod +x /cosign

FROM scratch
COPY --from=downloader /cosign /cosign
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /cosign && chmod +x /cosign
RUN mkdir -p /app /var/log/cosign /var/cache/cosign && chown 65534:65534 /app /var/log/cosign /var/cache/cosign
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:8080/cosign version || exit 1
ENTRYPOINT ["/cosign"]
LABEL org.opencontainers.image.title="cosign" \
      org.opencontainers.image.version="2.4.0" \
      org.opencontainers.image.vendor="Sigstore" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
