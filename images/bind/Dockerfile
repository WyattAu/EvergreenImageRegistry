# =============================================================================
# SOVEREIGN HARDENED BIND
# Generated from template - Version: 9.18.0
# =============================================================================

ARG VERSION=9.18.0
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://www.isc.org/bind/" -o /named.tar.gz && \
    tar -xzf /named.tar.gz -C / && rm /named.tar.gz && chmod +x /named

FROM scratch
COPY --from=downloader /named /named
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /named && chmod +x /named
RUN mkdir -p /app /var/log/named /var/cache/named && chown 65534:65534 /app /var/log/named /var/cache/named
USER 65534:65534
WORKDIR /app
EXPOSE 53 953
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:53/- || exit 1
ENTRYPOINT ["/named"]
LABEL org.opencontainers.image.title="bind" \
      org.opencontainers.image.version="9.18.0" \
      org.opencontainers.image.vendor="ISC" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
