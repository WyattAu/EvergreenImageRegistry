# =============================================================================
# SOVEREIGN HARDENED SYFT
# Generated from template - Version: 1.8.0
# =============================================================================

ARG VERSION=1.8.0
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://github.com/anchore/syft/releases/download/v1.8.0/syft_1.8.0_linux_amd64.tar.gz" -o /syft.tar.gz && \
    tar -xzf /syft.tar.gz -C / && rm /syft.tar.gz && chmod +x /syft

FROM scratch
COPY --from=downloader /syft /syft
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /syft && chmod +x /syft
RUN mkdir -p /app /var/log/syft /var/cache/syft && chown 65534:65534 /app /var/log/syft /var/cache/syft
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:8080/syft version || exit 1
ENTRYPOINT ["/syft"]
LABEL org.opencontainers.image.title="syft" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Anchore" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
