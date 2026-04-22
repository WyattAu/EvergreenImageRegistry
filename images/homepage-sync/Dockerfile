FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/benphelps/homepage/releases/download/v0.9.3/homepage_0.9.3_linux_amd64.tar.gz" \
    -o /homepage.tar.gz && \
    tar -xzf /homepage.tar.gz -C / && rm /homepage.tar.gz && chmod +x /homepage 2>/dev/null || true
RUN strip /homepage 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/homepage /var/cache/homepage

FROM debian:bookworm-slim
COPY --from=downloader /homepage /usr/local/bin/homepage
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin homepage 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["homepage", "--version"]
ENTRYPOINT ["homepage"]
CMD ["--config", "/app/config", "--enable-sync"]
LABEL org.opencontainers.image.title="homepage-sync" \
      org.opencontainers.image.description="Homepage - sync mode" \
      org.opencontainers.image.vendor="benphelps" \
      org.opencontainers.image.source="https://github.com/benphelps/homepage" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
