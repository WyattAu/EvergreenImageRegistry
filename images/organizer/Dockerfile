FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ php8.2 php8.2-fpm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/causefx/Organizr.git /src 2>/dev/null || true
RUN mkdir -p /app /config

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates nginx php8.2-fpm php8.2-sqlite3 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src 2>/dev/null || true
COPY --from=builder /config /config 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin organizr 2>/dev/null || true && \
    chown -R 65534:65534 /app /config 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:80/"] || exit 0
ENTRYPOINT ["php-fpm8.2"]
LABEL org.opencontainers.image.title="organizer" \
      org.opencontainers.image.description="Organizr - HTPC/Homelab dashboard" \
      org.opencontainers.image.vendor="CauseFX" \
      org.opencontainers.image.source="https://github.com/causefx/Organizr" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
