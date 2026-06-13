ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM cgr.dev/chainguard/wolfi-base AS builder

ARG VERSION=1.27.1
ARG TARGETARCH

RUN apk add --no-cache gcc make pcre2-dev zlib-dev linux-headers ca-certificates wget

WORKDIR /src
RUN wget -q "https://nginx.org/download/nginx-${VERSION}.tar.gz" -O nginx.tar.gz && \
    tar -xzf nginx.tar.gz && rm nginx.tar.gz

RUN cd nginx-${VERSION} && \
    ./configure \
        --prefix=/etc/nginx \
        --sbin-path=/nginx \
        --without-http_rewrite_module \
        --without-http_gzip_module \
        --with-cc-opt="-static" \
        --with-ld-opt="-static" && \
    make -j$(nproc) && \
    make install

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim
COPY --from=builder /nginx /nginx
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY shim.toml /etc/evergreen/shim.toml
USER ${APP_UID}:${APP_GID}
ENV SHIM_METRICS_ENABLED="true" \
    SHIM_MANAGEMENT_ENABLED="true" \
    SHIM_MANAGEMENT_HOST="0.0.0.0" \
    SHIM_MANAGEMENT_PORT="9102"
WORKDIR /
EXPOSE 80 443 9101 9102

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/shim", "run", "-c", "/nginx"]
LABEL org.opencontainers.image.title="nginx" \
      org.opencontainers.image.description="Nginx - HTTP and reverse proxy server" \
      org.opencontainers.image.version="1.27.1" \
      org.opencontainers.image.vendor="Nginx Inc" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.source="https://github.com/nginx/nginx" \
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
      evergreen.hft.xdp-capable="true" \
      evergreen.hft.xdp-mode="generic" \
      evergreen.hft.xdp-notes="Requires custom nginx module or eBPF loader"

LABEL evergreen.base.image="scratch" \
      evergreen.build.type="musl-source" \
      evergreen.metrics.native="ztunnel" \
      evergreen.health.type="http" \
      evergreen.health.endpoint="/livez" \
      evergreen.health.listen="0.0.0.0:9101" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
