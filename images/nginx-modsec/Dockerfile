FROM cgr.dev/chainguard/wolfi-base:latest
ARG NGINX_VERSION=1.27.1
ARG MODSEC_VERSION=3.0.12

RUN apk add --no-cache nginx ca-certificates libxml2 curl || true
RUN addgroup -S -g 10000 nginx 2>/dev/null || true && \
    adduser -u 65532 -G nginx -D -h /app -s /bin/false nginx 2>/dev/null || true
RUN mkdir -p /app /var/log/nginx /var/cache/nginx /etc/nginx/modsec /run 2>/dev/null || true
RUN chown -R 65532:65532 /app /var/log/nginx /var/cache/nginx 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80 443
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
LABEL org.opencontainers.image.title="nginx-modsec" \
      org.opencontainers.image.version="1.27.1" \
      org.opencontainers.image.vendor="NGINX Inc / SpiderLabs" \
      org.opencontainers.image.source="https://github.com/SpiderLabs/ModSecurity" \
      org.opencontainers.image.description="NGINX with ModSecurity WAF module" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
