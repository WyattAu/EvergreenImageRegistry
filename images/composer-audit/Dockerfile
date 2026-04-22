FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        php8.2 php8.2-cli php8.2-mbstring php8.2-xml php8.2-curl \
        ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://getcomposer.org/installer" | php -- --install-dir=/usr/local/bin --filename=composer
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        php8.2 php8.2-cli php8.2-mbstring php8.2-xml php8.2-curl \
        ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/bin/composer /usr/local/bin/composer
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin composer 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["composer", "--version"]
ENTRYPOINT ["composer"]
CMD ["audit"]
LABEL org.opencontainers.image.title="composer-audit" \
      org.opencontainers.image.description="Composer audit - PHP dependency security scanner" \
      org.opencontainers.image.vendor="Composer" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
