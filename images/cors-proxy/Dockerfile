ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







ARG NGINX_VERSION=1.25.5







RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    curl ca-certificates \
    build-essential libpcre2-dev zlib1g-dev && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" -o /nginx.tar.gz && \
    echo "2fe2294f8af4144e7e842eaea884182a84ee7970e11046ba98194400902bbec0  /nginx.tar.gz" | sha256sum -c; \
    curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz.asc" -o /nginx.tar.gz.asc && \
    [ -f /nginx.tar.gz ] && tar -xzf /nginx.tar.gz -C /tmp/ ; \
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
    make -j"$(nproc)" ; \ \
    make install ; \
RUN mkdir -p /opt/nginx/sbin \
       strip --strip-all /opt/nginx/sbin/nginx 2>/dev/null&& \
    rm -rf /nginx.tar.gz /nginx.tar.gz.asc /tmp/nginx-${NGINX_VERSION} && \
    mkdir -p /opt/nginx 2>/dev/null || true







FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim
















RUN apk add --no-cache libpcre2-8-0 zlib ca-certificates















COPY --from=builder /opt/nginx /opt/nginx















RUN mkdir -p /app/logs /app/conf ; 2>/dev/null || true ; \
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







RUN if ($request_method = 'OPTIONS') {







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
ENV SHIM_METRICS_ENABLED="true"







WORKDIR /app







EXPOSE 8080






















HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]







CMD ["-c", "/opt/nginx/sbin/nginx", "--", "-c", "/app/conf/nginx.conf", "-g", "daemon off;"]







LABEL org.opencontainers.image.title="cors-proxy" \
      org.opencontainers.image.description="cors-proxy container image" \
      org.opencontainers.image.version="1.25.5" \
      org.opencontainers.image.vendor="nginx" \
      org.opencontainers.image.source="https://nginx.org" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distrole="debian-slim" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"







LABEL evergreen.base.image="wolfi"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
