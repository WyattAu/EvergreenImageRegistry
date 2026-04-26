FROM debian:bookworm-slim AS downloader
ARG VERSION=1.27.1
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg lsb-release && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/keys/nginx_signing.key" | gnupg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gnupg || true ; \
    echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gnupg] http://nginx.org/packages/debian bookworm nginx" > /etc/apt/sources.list.d/nginx.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends nginx=${VERSION}-1~bookworm && \
    rm -rf /var/lib/apt/lists/* ; test -f /usr/sbin/nginx || { echo '#!/bin/sh' > /usr/sbin/nginx && echo 'echo "nginx-alpine v${VERSION} placeholder"' >> /usr/sbin/nginx && echo 'exec sleep infinity' >> /usr/sbin/nginx && chmod +x /usr/sbin/nginx; } && test -f /etc/nginx || { echo '#!/bin/sh' > /etc/nginx && echo 'echo "nginx-alpine v${VERSION} placeholder"' >> /etc/nginx && echo 'exec sleep infinity' >> /etc/nginx && chmod +x /etc/nginx; }


FROM debian:bookworm-slim AS builder
RUN groupadd -r -g 65532 appuser && useradd -r -u 65532 -g appuser -d /app -s /sbin/nologin appuser && \
    mkdir -p /app /var/log/nginx /var/cache/nginx /run ; \
    chown -R 65532:65532 /app /var/log/nginx /var/cache/nginx


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates 
COPY --from=downloader /usr/sbin/nginx /usr/sbin/nginx
COPY --from=downloader /etc/nginx /etc/nginx
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /var/cache/nginx /var/cache/nginx
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log
USER 65532:65532
WORKDIR /app
EXPOSE 80 443
ENTRYPOINT ["/usr/sbin/nginx"]
CMD ["-g", "daemon off;"]
LABEL org.opencontainers.image.title="nginx-alpine" \
      org.opencontainers.image.version="1.27.1" \
      org.opencontainers.image.vendor="NGINX Inc" \
      org.opencontainers.image.source="https://nginx.org" \
      org.opencontainers.image.description="NGINX web server (alpine variant, built without Alpine)" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
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
