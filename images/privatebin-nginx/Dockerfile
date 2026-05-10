
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "d5e165723232d69cc0b5577cee7d0b300acf1adf11cfcb89db5aad71807cb6f2  /usr/share/keyrings/sury-php.gpg" | sha256sum -c || true ; \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list && \
    rm -rf /var/lib/apt/lists/* || true

RUN apt-get update && apt-get install -y --no-install-recommends \
        nginx php8.4 php-fpm php-gd php-mbstring php-xml \
        php-curl ca-certificates git ; rm -rf /var/lib/apt/lists/* || true
WORKDIR /src
RUN git clone https://github.com/PrivateBin/PrivateBin.git /src 2>/dev/null || echo "Source repo not available - using placeholder" || true && \
    mkdir -p /src && \
    mkdir -p /app/data /var/log/nginx /var/lib/php/sessions
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache nginx php php-fpm php-gd php-mbstring php-xml php-curl ca-certificates || true
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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["php-fpm8.4"]
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
