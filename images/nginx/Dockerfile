ARG VERSION=1.27.1
ARG SHIM_VERSION=v2.0.0

# Extract nginx binary from official image
FROM nginx:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base
COPY --from=shim /shim /usr/local/bin/shim

# Install nginx via apk (more reliable than extraction)
RUN apk add --no-cache nginx ca-certificates && \
    mkdir -p /var/log/nginx /var/cache/nginx /var/run /etc/nginx/conf.d && \
    chown -R 65532:65532 /var/log/nginx /var/cache/nginx /var/run /etc/nginx

# Minimal nginx config
RUN printf 'events {}\nhttp {\n  server {\n    listen 8080;\n    root /usr/share/nginx/html;\n    index index.html;\n  }\n}\n' > /etc/nginx/nginx.conf && \
    mkdir -p /usr/share/nginx/html && \
    echo "<h1>Evergreen Nginx</h1>" > /usr/share/nginx/html/index.html && \
    chown -R 65532:65532 /usr/share/nginx /etc/nginx/nginx.conf

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

EXPOSE 8080 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "nginx"]

LABEL org.opencontainers.image.title="nginx" \
      org.opencontainers.image.description="Nginx - wolfi-base, non-root, with health-shim" \
      org.opencontainers.image.version="${VERSION}" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
