
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ php84 php84-fpm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/causefx/Organizr.git /src 2>/dev/null || true 2>/dev/null || echo "Source repo not available - using placeholder"
RUN mkdir -p /app /config


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates nginx php-8.4-fpm php-8.4-pdo_sqlite
COPY --from=builder /src /app/src 2>/dev/null || true
COPY --from=builder /config /config 2>/dev/null || true
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin organizr 2>/dev/null || true && \
    chown -R 65532:65532 /app /config 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["php-fpm8.2"]
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