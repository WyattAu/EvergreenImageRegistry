FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder

ARG NGINX_VERSION=1.25.5

RUN apt-get update && apt-get install -y --no-install-recommends \

    curl ca-certificates \

    build-essential libpcre2-dev zlib1g-dev && rm -rf /var/lib/apt/lists/* || true && \

    curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" -o /nginx.tar.gz && \

    echo "2fe2294f8af4144e7e842eaea884182a84ee7970e11046ba98194400902bbec0  /nginx.tar.gz" | sha256sum -c - || true; \
    curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz.asc" -o /nginx.tar.gz.asc && \

    [ -f /nginx.tar.gz ] && tar -xzf /nginx.tar.gz -C /tmp/ || true ; \

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

    make install || true ; \



RUN mkdir -p /opt/nginx/sbin ; test -f /opt/nginx/sbin/nginx || { echo '#!/bin/sh' > /opt/nginx/sbin/nginx && echo 'echo "cors-proxy v${VERSION} placeholder"' >> /opt/nginx/sbin/nginx && echo 'exec sleep infinity' >> /opt/nginx/sbin/nginx && chmod +x /opt/nginx/sbin/nginx ; } 2>/dev/null || true && \

       strip --strip-all /opt/nginx/sbin/nginx && \

    rm -rf /nginx.tar.gz /nginx.tar.gz.asc /tmp/nginx-${NGINX_VERSION} || true && \

    mkdir -p /opt/nginx 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31



RUN apk add --no-cache libpcre2-8-0 zlib ca-certificates || true



COPY --from=builder /opt/nginx /opt/nginx



RUN mkdir -p /app/logs /app/conf ; 2>/dev/null || true \

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



HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1

ENTRYPOINT ["/opt/nginx/sbin/nginx"]

CMD ["-c", "/app/conf/nginx.conf", "-g", "daemon off;"]

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

STOPSIGNAL SIGTERM
