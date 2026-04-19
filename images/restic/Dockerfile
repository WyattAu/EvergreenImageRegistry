# =============================================================================
# SOVEREIGN HARDENED RESTIC
# Generated from template - Version: 0.17.0
# =============================================================================

ARG VERSION=0.17.0
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://github.com/restic/restic/releases/download/v0.17.0/restic_0.17.0_linux_amd64.tar.gz" -o /restic.tar.gz && \
    tar -xzf /restic.tar.gz -C / && rm /restic.tar.gz && chmod +x /restic

FROM scratch
COPY --from=downloader /restic /restic
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /restic && chmod +x /restic
RUN mkdir -p /app /var/log/restic /var/cache/restic && chown 65534:65534 /app /var/log/restic /var/cache/restic
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:8080/restic version || exit 1
ENTRYPOINT ["/restic"]
LABEL org.opencontainers.image.title="restic" \
      org.opencontainers.image.version="0.17.0" \
      org.opencontainers.image.vendor="Restic" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
