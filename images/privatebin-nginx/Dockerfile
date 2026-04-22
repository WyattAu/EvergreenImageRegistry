FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nginx php8.2 php8.2-fpm php8.2-gd php8.2-mbstring php8.2-xml \
        php8.2-curl ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/PrivateBin/PrivateBin.git /src
RUN mkdir -p /app/data /var/log/nginx /var/lib/php/sessions

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nginx php8.2 php8.2-fpm php8.2-gd php8.2-mbstring php8.2-xml \
        php8.2-curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app/data /app/data
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /var/lib/php/sessions /var/lib/php/sessions
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin privatebin 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/nginx /var/lib/php/sessions 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:80/"] || exit 0
ENTRYPOINT ["php-fpm8.2"]
LABEL org.opencontainers.image.title="privatebin-nginx" \
      org.opencontainers.image.description="PrivateBin - encrypted pastebin with nginx" \
      org.opencontainers.image.vendor="PrivateBin" \
      org.opencontainers.image.source="https://github.com/PrivateBin/PrivateBin" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
