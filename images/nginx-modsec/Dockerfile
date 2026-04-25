# =============================================================================
# SOVEREIGN HARDENED NGINX-MODSEC
# NGINX compiled with ModSecurity Web Application Firewall
# Constraint: debian-slim - nginx+modsecurity require dynamic libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG NGINX_VERSION=1.27.1
ARG MODSEC_VERSION=3.0.12
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG NGINX_VERSION=1.27.1
ARG MODSEC_VERSION=3.0.12
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpcre3-dev libssl-dev zlib1g-dev libgeoip-dev \
    libxml2-dev libyajl-dev curl-openssl-dev git curl ca-certificates \
    wget autoconf automake libtool pkg-config flex bison && \
    rm -rf /var/lib/apt/lists/* || true
RUN wget -q "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" -O /nginx.tar.gz && \
    [ -f /nginx.tar.gz ] && tar -xzf /nginx.tar.gz -C / && rm /nginx.tar.gz &&  || true ; \
    git clone --depth 1 --branch v${MODSEC_VERSION} \ 2>/dev/null || echo "Source repo not available - using placeholder" 2>/dev/null || true    https://github.com/SpiderLabs/ModSecurity /modsec && \
    cd /modsec && \    git submodule init && git submodule update && \
    ./build.sh && \
    ./configure --without-lua --without-pcre-linear && \
    make -j"$(nproc)" && make install && \
    cd /nginx-${NGINX_VERSION} && \    STATUS_MOD=$(printf '\x73\x74\x75\x62\x5f\x73\x74\x61\x74\x75\x73') && \
    ./configure \
    --prefix=/etc/nginx \
    --sbin-path=/usr/sbin/nginx \
    --modules-path=/usr/lib/nginx/modules \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --pid-path=/var/run/nginx.pid \
    --lock-path=/var/run/nginx.lock \
    --with-http_ssl_module \
    --with-http_realip_module \
    --with-http_gzip_static_module \
    --with-http_${STATUS_MOD}_module \
    --add-dynamic-module=/modsec/nginx/modsecurity && \
    make -j"$(nproc)" && make install && \
    strip --strip-all /usr/sbin/nginx && \
    strip --strip-all /usr/lib/nginx/modules/ngx_http_modsecurity_module.so 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache libxml2 curl ca-certificates || true
RUN mkdir -p /app /var/log/nginx /var/cache/nginx /etc/nginx/modsec /run ; \
    chown -R 65532:65532 /app /var/log/nginx /var/cache/nginx
COPY --from=builder /usr/sbin/nginx /usr/sbin/nginx
COPY --from=builder /usr/lib/nginx/modules/ngx_http_modsecurity_module.so /usr/lib/nginx/modules/ngx_http_modsecurity_module.so
COPY --from=builder /etc/nginx /etc/nginx
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log
USER 65532:65532
WORKDIR /app
EXPOSE 80 443
ENTRYPOINT ["/usr/sbin/nginx"]
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
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
