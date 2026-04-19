# =============================================================================
# SOVEREIGN HARDENED COREDNS
# Generated from template - Version: 1.12.0
# =============================================================================

ARG VERSION=1.12.0
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://github.com/coredns/coredns/releases/download/v1.12.0/coredns_1.12.0_linux_amd64.tgz" -o /coredns.tar.gz && \
    tar -xzf /coredns.tar.gz -C / && rm /coredns.tar.gz && chmod +x /coredns

FROM scratch
COPY --from=downloader /coredns /coredns
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /coredns && chmod +x /coredns
RUN mkdir -p /app /var/log/coredns /var/cache/coredns && chown 65534:65534 /app /var/log/coredns /var/cache/coredns
USER 65534:65534
WORKDIR /app
EXPOSE 53
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:53//health || exit 1
ENTRYPOINT ["/coredns"]
LABEL org.opencontainers.image.title="coredns" \
      org.opencontainers.image.version="1.12.0" \
      org.opencontainers.image.vendor="Coredns" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
