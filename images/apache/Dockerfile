# =============================================================================
# SOVEREIGN HARDENED APACHE
# Generated from template - Version: 2.4.61
# =============================================================================

ARG VERSION=2.4.61
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://httpd.apache.org/" -o /httpd.tar.gz && \
    tar -xzf /httpd.tar.gz -C / && rm /httpd.tar.gz && chmod +x /httpd

FROM scratch
COPY --from=downloader /httpd /httpd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /httpd && chmod +x /httpd
RUN mkdir -p /app /var/log/httpd /var/cache/httpd && chown 65534:65534 /app /var/log/httpd /var/cache/httpd
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:80// || exit 1
ENTRYPOINT ["/httpd"]
LABEL org.opencontainers.image.title="apache" \
      org.opencontainers.image.version="2.4.61" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
