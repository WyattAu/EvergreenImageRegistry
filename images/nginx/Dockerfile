# =============================================================================
# SOVEREIGN HARDENED NGINX
# Generated from template - Version: 1.27.1
# =============================================================================

ARG VERSION=1.27.1
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://nginx.org/download/nginx-1.27.1.tar.gz" -o /nginx.tar.gz && \
    tar -xzf /nginx.tar.gz -C / && rm /nginx.tar.gz

# Note: Building nginx from source requires compiler - using official base instead
# For production, use official nginx:alpine and apply hardening
FROM nginx:1.27-alpine
RUN apk add --no-cache ca-certificates
RUN rm -rf /var/cache/apk/* /etc/nginx/conf.d/* /var/log/nginx/* /var/tmp/*
RUN adduser -D -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/nginx /var/cache/nginx && chown -R app:app /app /var/log/nginx /var/cache/nginx
USER app
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:80/ || exit 1
ENTRYPOINT ["nginx", "-g", "daemon off;"]
LABEL org.opencontainers.image.title="nginx" \
      org.opencontainers.image.version="1.27.1" \
      org.opencontainers.image.vendor="Nginx Inc" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"