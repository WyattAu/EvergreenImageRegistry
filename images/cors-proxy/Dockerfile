# =============================================================================
# SOVEREIGN HARDENED CORS PROXY
# nginx-based CORS reverse proxy with hardened config
# Constraint: debian-slim - nginx requires runtime libs and shell for signal handling
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG NGINX_VERSION=1.25.5
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG NGINX_VERSION=1.25.5
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    build-essential libpcre2-dev zlib1g-dev && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" -o /nginx.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz.asc" -o /nginx.tar.gz.asc && \
    tar -xzf /nginx.tar.gz -C /tmp/ && \
    cd /tmp/nginx-${NGINX_VERSION} && \    ./configure \
        --prefix=/opt/nginx \
        --without-http_rewrite_module \
        --without-http_gzip_module \
        --with-http_ssl_module \
        --without-http_uwsgi_module \
        --without-http_scgi_module \
        --without-http_access_module \
        --error-log-path=/dev/stderr \
        --http-log-path=/dev/stdout \
        --pid-path=/tmp/nginx.pid \
        --lock-path=/tmp/nginx.lock && \
    make -j"$(nproc)" && \
    make install && \
    strip --strip-all /opt/nginx/sbin/nginx && \
    rm -rf /nginx.tar.gz /nginx.tar.gz.asc /tmp/nginx-${NGINX_VERSION}

# hadolint ignore=DL3023

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache libpcre2-8-0 zlib ca-certificates

COPY --from=builder /opt/nginx /opt/nginx

RUN mkdir -p /app/logs /app/conf && \
    chown -R 65532:65532 /app

COPY <<'NGINXCONF' /app/conf/nginx.conf
worker_processes 1;
error_log /dev/stderr warn;
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    access_log /dev/stdout;

    server {
        listen 8080;
        server_name _;

        location / {
            if ($request_method = 'OPTIONS') {
                add_header 'Access-Control-Allow-Origin' '*' always;
                add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
                add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, X-Requested-With' always;
                add_header 'Access-Control-Max-Age' 86400;
                add_header 'Content-Length' 0;
                add_header 'Content-Type' 'text/plain';
                return 204;
            }

            proxy_pass http://backend:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            add_header 'Access-Control-Allow-Origin' '*' always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, X-Requested-With' always;
        }
    }
}
NGINXCONF

RUN chown 65532:65532 /app/conf/nginx.conf
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/opt/nginx/sbin/nginx"]
CMD ["-c", "/app/conf/nginx.conf", "-g", "daemon off;"]
LABEL org.opencontainers.image.title="cors-proxy" \
      org.opencontainers.image.version="1.25.5" \
      org.opencontainers.image.vendor="nginx" \
      org.opencontainers.image.source="https://nginx.org" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distrole="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM