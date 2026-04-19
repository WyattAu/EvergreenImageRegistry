# =============================================================================
# SOVEREIGN HARDENED NGINX
# Generated from template - Version: 1.27.1
# =============================================================================

ARG VERSION=1.27.1
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://nginx.org/download/nginx-1.27.1.tar.gz" -o /nginx.tar.gz && \
    tar -xzf /nginx.tar.gz -C / && rm /nginx.tar.gz && chmod +x /nginx

FROM scratch
COPY --from=downloader /nginx /nginx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /nginx && chmod +x /nginx
RUN mkdir -p /app /var/log/nginx /var/cache/nginx && chown 65534:65534 /app /var/log/nginx /var/cache/nginx
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:80//health_status.html || exit 1
ENTRYPOINT ["/nginx"]
LABEL org.opencontainers.image.title="nginx" \
      org.opencontainers.image.version="1.27.1" \
      org.opencontainers.image.vendor="Nginx Inc" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
