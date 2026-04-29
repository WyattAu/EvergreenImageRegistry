FROM debian:bookworm-slim AS downloader
ARG VERSION=1.12.16
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /tmp
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/element-hq/element-web/releases/download/v${VERSION}/element-v${VERSION}.tar.gz -o /tmp/release.tar.gz && \
    mkdir -p /www-src && \
    tar -xzf /tmp/release.tar.gz -C /www-src --strip-components=1 && \
    rm /tmp/release.tar.gz


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates 
RUN addgroup -S -g 65532 appuser && adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser || true
COPY --from=downloader /www-src /var/www/html
RUN rm -f /etc/nginx/sites-enabled/default
RUN printf 'server {\
n    listen 8080 default_server;\
n    root /var/www/html;\
n    index index.html;\
n    location / { try_files $uri $uri/ =404; }\
n}\
n' > /etc/nginx/sites-available/default && \
    ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default && \
    chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx
USER 65532:65532
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
LABEL org.opencontainers.image.title="element-web" \
      org.opencontainers.image.description="Element Web - web client for Matrix" \
      org.opencontainers.image.version="1.12.16" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/element-web" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
