
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/log/nginx || true
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "d5e165723232d69cc0b5577cee7d0b300acf1adf11cfcb89db5aad71807cb6f2  /usr/share/keyrings/sury-php.gpg" | sha256sum -c ; \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list && \
    rm -rf /var/lib/apt/lists/* || true

RUN apt-get update && apt-get install -y --no-install-recommends \
        nginx php8.4 php-fpm php-gd php-mbstring php-xml \
        php-curl ca-certificates git ; rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone https://github.com/PrivateBin/PrivateBin.git /src 2>/dev/null || { echo "Binary not available - download failed" >&2; exit 1; } && \
    mkdir -p /src && \
    mkdir -p /app/data /var/log/nginx /var/lib/php/sessions
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache nginx php-8.4 php-8.4-fpm php-8.4-gd php-8.4-mbstring php-8.4-xml php-8.4-curl ca-certificates
COPY --from=builder /src /app/src
COPY --from=builder /app/data /app/data
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /var/lib/php/sessions /var/lib/php/sessions
RUN addgroup -S nogroup || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false privatebin || true && \
    chown -R 65532:65532 /app /var/log/nginx /var/lib/php/sessions 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="privatebin-nginx" \
      org.opencontainers.image.description="PrivateBin - encrypted pastebin with nginx" \
      org.opencontainers.image.vendor="PrivateBin" \
      org.opencontainers.image.source="https://github.com/PrivateBin/PrivateBin" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
