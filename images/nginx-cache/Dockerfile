ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG VERSION=1.27.1
ARG TARGETARCH







RUN mkdir -p /etc/nginx || true
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg lsb-release && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://nginx.org/keys/nginx_signing.key" | gpg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gnupg 2>/dev/null ; \
    echo "55385da31d198fa6a5012d40ae98ecb272a6c4e8fffffba94719ffd3e87de37a  /usr/share/keyrings/nginx-archive-keyring.gnupg" | sha256sum -c; \
    echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gnupg] http://nginx.org/packages/debian bookworm nginx" > /etc/apt/sources.list.d/nginx.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends nginx=${VERSION}-1~bookworm && \
    rm -rf /var/lib/apt/lists/*























FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /app /var/log/nginx /var/cache/nginx/proxy /var/cache/nginx/fastcgi /run ; \
    chown -R 65532:65532 /app /var/log/nginx /var/cache/nginx























FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim
















RUN apk add --no-cache ca-certificates








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
ENV SHIM_METRICS_ENABLED="true"







WORKDIR /app







EXPOSE 80 443






















HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]







CMD ["-c", "/usr/sbin/nginx", "--", "-g", "daemon off;"]







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







LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
