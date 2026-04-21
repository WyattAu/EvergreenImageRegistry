# =============================================================================
# SOVEREIGN HARDENED BASIC AUTH PROXY
# nginx-based basic authentication reverse proxy
# Constraint: debian-slim - nginx requires runtime libs
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG NGINX_VERSION=1.25.5
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    build-essential libpcre2-dev zlib1g-dev && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" -o /nginx.tar.gz && \
    tar -xzf /nginx.tar.gz -C /tmp/ && \
    cd /tmp/nginx-${NGINX_VERSION} && \
    ./configure \
        --prefix=/opt/nginx \
        --without-http_rewrite_module \
        --without-http_gzip_module \
        --with-http_ssl_module \
        --without-http_uwsgi_module \
        --without-http_scgi_module \
        --with-http_auth_basic_module \
        --error-log-path=/dev/stderr \
        --http-log-path=/dev/stdout \
        --pid-path=/tmp/nginx.pid \
        --lock-path=/tmp/nginx.lock && \
    make -j"$(nproc)" && \
    make install && \
    strip --strip-all /opt/nginx/sbin/nginx && \
    rm -rf /nginx.tar.gz /tmp/nginx-${NGINX_VERSION}

# hadolint ignore=DL3023
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpcre2-8-0 zlib1g ca-certificates apache2-utils && rm -rf /var/lib/apt/lists/* && \
    groupadd -g 65534 nginx && useradd -u 65534 -g nginx -s /usr/sbin/nologin -d /app nginx

COPY --from=builder /opt/nginx /opt/nginx

RUN mkdir -p /app/logs /app/conf && \
    chown -R 65534:65534 /app

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
            auth_basic "Restricted";
            auth_basic_user_file /app/conf/.htpasswd;

            proxy_pass http://backend:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
NGINXCONF

RUN chown 65534:65534 /app/conf/nginx.conf && \
    touch /app/conf/.htpasswd && chown 65534:65534 /app/conf/.htpasswd

USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/opt/nginx/sbin/nginx", "-t"]
ENTRYPOINT ["/opt/nginx/sbin/nginx"]
CMD ["-c", "/app/conf/nginx.conf", "-g", "daemon off;"]
LABEL org.opencontainers.image.title="basic-auth-proxy" \
      org.opencontainers.image.version="1.25.5" \
      org.opencontainers.image.vendor="nginx" \
      org.opencontainers.image.source="https://nginx.org" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distrole="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
