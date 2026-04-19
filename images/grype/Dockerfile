# =============================================================================
# SOVEREIGN HARDENED GRYPE
# Generated from template - Version: 0.80.0
# =============================================================================

ARG VERSION=0.80.0
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://github.com/anchore/grype/releases/download/v0.80.0/grype_0.80.0_linux_amd64.tar.gz" -o /grype.tar.gz && \
    tar -xzf /grype.tar.gz -C / && rm /grype.tar.gz && chmod +x /grype

FROM scratch
COPY --from=downloader /grype /grype
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /grype && chmod +x /grype
RUN mkdir -p /app /var/log/grype /var/cache/grype && chown 65534:65534 /app /var/log/grype /var/cache/grype
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:8080/grype version || exit 1
ENTRYPOINT ["/grype"]
LABEL org.opencontainers.image.title="grype" \
      org.opencontainers.image.version="0.80.0" \
      org.opencontainers.image.vendor="Anchore" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
