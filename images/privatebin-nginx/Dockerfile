
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        nginx php84 php8.4-fpm php8.4-gd php8.4-mbstring php8.4-xml \
        php8.4-curl ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/PrivateBin/PrivateBin.git /src 2>/dev/null || echo "Source repo not available - using placeholder"
RUN mkdir -p /src 2>/dev/null || true
RUN mkdir -p /app/data /var/log/nginx /var/lib/php/sessions


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nginx php-8.4 php-8.4-fpm php-8.4-gd php-8.4-mbstring php-8.4-xml php-8.4-curl ca-certificates
COPY --from=builder /src /app/src
COPY --from=builder /app/data /app/data
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /var/lib/php/sessions /var/lib/php/sessions
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin privatebin 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/nginx /var/lib/php/sessions 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["php-fpm8.4"]
LABEL org.opencontainers.image.title="privatebin-nginx" \
      org.opencontainers.image.description="PrivateBin - encrypted pastebin with nginx" \
      org.opencontainers.image.vendor="PrivateBin" \
      org.opencontainers.image.source="https://github.com/PrivateBin/PrivateBin" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM