# =============================================================================
# SOVEREIGN HARDENED UNBOUND
# Generated from template - Version: 1.20.0
# =============================================================================

ARG VERSION=1.20.0
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://unbound.net/" -o /unbound.tar.gz && \
    tar -xzf /unbound.tar.gz -C / && rm /unbound.tar.gz && chmod +x /unbound

FROM scratch
COPY --from=downloader /unbound /unbound
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /unbound && chmod +x /unbound
RUN mkdir -p /app /var/log/unbound /var/cache/unbound && chown 65534:65534 /app /var/log/unbound /var/cache/unbound
USER 65534:65534
WORKDIR /app
EXPOSE 53
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:53/- || exit 1
ENTRYPOINT ["/unbound"]
LABEL org.opencontainers.image.title="unbound" \
      org.opencontainers.image.version="1.20.0" \
      org.opencontainers.image.vendor="NLnet Labs" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
