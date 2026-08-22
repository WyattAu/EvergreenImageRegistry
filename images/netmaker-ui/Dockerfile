ARG VERSION=v1.5.1
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM gravitl/netmaker-ui:latest AS upstream

FROM cgr.dev/chainguard/wolfi-base
COPY --from=ghcr.io/wyattau/evergreenshim/health-shim:v2.0.0 /shim /usr/local/bin/shim
RUN apk add --no-cache nginx ca-certificates && \
    mkdir -p /var/log/nginx /var/cache/nginx /var/run /etc/nginx/conf.d /www && \
    chown -R 65532:65532 /var/log/nginx /var/cache/nginx /var/run /www
COPY --from=upstream /usr/share/nginx/html /www

# Minimal nginx config for serving static SPA
RUN printf 'events {}\nhttp {\n  server {\n    listen 8080;\n    root /www;\n    index index.html;\n    location / {\n      try_files $uri $uri/ /index.html;\n    }\n  }\n}\n' > /etc/nginx/nginx.conf && \
    chown -R 65532:65532 /etc/nginx/nginx.conf

USER 65532:65532
WORKDIR /www
EXPOSE 8080 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "nginx"]
LABEL org.opencontainers.image.title="netmaker-ui" \
      org.opencontainers.image.version="v1.5.1" \
      org.opencontainers.image.source="https://github.com/gravitl/netmaker-ui" \
      org.opencontainers.image.description="Netmaker UI - static web interface served by nginx" \
      evergreen.base.image="wolfi"
LABEL evergreen.image.tier="standard"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
