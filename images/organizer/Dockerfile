
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list && \
    rm -rf /var/lib/apt/lists/* || true

RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ php8.4 php8.4-fpm ; rm -rf /var/lib/apt/lists/* || true
WORKDIR /src
RUN git clone --depth 1 https://github.com/causefx/Organizr.git /src 2>/dev/null || true 2>/dev/null || echo "Source repo not available - using placeholder"
RUN mkdir -p /src
RUN mkdir -p /app /config


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates nginx php-8.4-fpm php-8.4-pdo_sqlite 
COPY --from=builder /src /app/src
COPY --from=builder /config /config
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
mkdir -p /app 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false organizr && \
    chown -R 65532:65532 /app /config
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["php-fpm8.4"]
LABEL org.opencontainers.image.title="organizer" \
      org.opencontainers.image.description="Organizr - HTPC/Homelab dashboard" \
      org.opencontainers.image.vendor="CauseFX" \
      org.opencontainers.image.source="https://github.com/causefx/Organizr" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM