FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        php84 php84 php84-php84-mbstring php84-php84-xml php84-curl \
        ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://getcomposer.org/installer" | php -- --install-dir=/usr/local/bin --filename=composer
RUN mkdir -p /app

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache php-8.4 php-8.4-mbstring php-8.4-xml php-8.4-curl ca-certificates curl unzip
COPY --from=builder /usr/local/bin/composer /usr/local/bin/composer
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin composer 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["composer"]
CMD ["audit"]
LABEL org.opencontainers.image.title="composer-audit" \
      org.opencontainers.image.description="Composer audit - PHP dependency security scanner" \
      org.opencontainers.image.vendor="Composer" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM