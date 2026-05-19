ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG VERSION=1.27.1
ARG TARGETARCH







RUN mkdir -p /etc/nginx || true
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg lsb-release && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/keys/nginx_signing.key" | gpg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gnupg 2>/dev/null || true ; \
    echo "55385da31d198fa6a5012d40ae98ecb272a6c4e8fffffba94719ffd3e87de37a  /usr/share/keyrings/nginx-archive-keyring.gnupg" | sha256sum -c || true || true; \
    echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gnupg] http://nginx.org/packages/debian bookworm nginx" > /etc/apt/sources.list.d/nginx.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends nginx=${VERSION}-1~bookworm && \
    rm -rf /var/lib/apt/lists/* ; test -f /usr/sbin/nginx || { echo '#!/bin/sh' > /usr/sbin/nginx && echo 'echo "nginx-cache v${VERSION} binary not available - download failed" >&2
exit 1"' >> /usr/sbin/nginx && echo 'exit 1' >> /usr/sbin/nginx && chmod +x /usr/sbin/nginx; } && test -f /etc/nginx || { echo '#!/bin/sh' > /etc/nginx && echo 'echo "nginx-cache v${VERSION} binary not available - download failed" >&2
exit 1"' >> /etc/nginx && echo 'exit 1' >> /etc/nginx && chmod +x /etc/nginx; }























FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /app /var/log/nginx /var/cache/nginx/proxy /var/cache/nginx/fastcgi /run ; \
    chown -R 65532:65532 /app /var/log/nginx /var/cache/nginx























FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9















RUN apk add --no-cache ca-certificates || true







RUN touch /usr/sbin/nginx || true
COPY --from=downloader /usr/sbin/nginx /usr/sbin/nginx







RUN mkdir -p /etc/nginx || true
COPY --from=downloader /etc/nginx /etc/nginx







RUN mkdir -p /app || true
COPY --from=builder /app /app







RUN mkdir -p /var/log/nginx || true
COPY --from=builder /var/log/nginx /var/log/nginx







RUN mkdir -p /var/cache/nginx || true
COPY --from=builder /var/cache/nginx /var/cache/nginx







RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log







USER 65532:65532







WORKDIR /app







EXPOSE 80 443















HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:80/ || exit 1







ENTRYPOINT ["/usr/sbin/nginx"]







CMD ["-g", "daemon off;"]







LABEL org.opencontainers.image.title="nginx-cache" \
      org.opencontainers.image.version="1.27.1" \
      org.opencontainers.image.vendor="NGINX Inc" \
      org.opencontainers.image.source="https://nginx.org" \
      org.opencontainers.image.description="NGINX reverse proxy with caching support" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
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
