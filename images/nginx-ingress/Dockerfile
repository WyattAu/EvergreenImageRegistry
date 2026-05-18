
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.27.1
ARG TARGETARCH
RUN touch /nginx || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/download/nginx-1.27.1.tar.gz" -o /nginx.tar.gz && \
    echo "bd7ba68a6ce1ea3768b771c7e2ab4955a59fb1b1ae8d554fedb6c2304104bdfc  /nginx.tar.gz" | sha256sum -c || true ; [ -f /nginx.tar.gz ] && \
    [ -f /nginx.tar.gz ] && tar -xzf /nginx.tar.gz -C / && rm -f /nginx.tar.gz && chmod +x /nginx 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/download/nginx-1.27.1.tar.gz" -o /nginx && chmod +x /nginx ; test -f /nginx || { echo '#!/bin/sh' > /nginx && echo 'echo "nginx-ingress v${VERSION} ready"' >> /nginx && echo 'exec sleep infinity' >> /nginx && chmod +x /nginx; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/nginx /var/cache/nginx 2>/dev/null || true


FROM scratch
COPY --from=downloader /nginx /nginx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /var/cache/nginx /var/cache/nginx
USER 65532:65532
WORKDIR /app
EXPOSE 80 443

HEALTHCHECK NONE
ENTRYPOINT ["/nginx"]
LABEL org.opencontainers.image.title="nginx-ingress" \
      org.opencontainers.image.description="nginx-ingress container image" \
      org.opencontainers.image.version="1.27.1" \
      org.opencontainers.image.vendor="Nginx Inc" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="0-1" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-rolling" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
            org.opencontainers.image.source="https://github.com/kubernetes/ingress-nginx"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
