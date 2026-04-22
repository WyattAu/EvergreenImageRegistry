FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/benphelps/homepage/releases/download/v0.9.3/homepage_0.9.3_linux_amd64.tar.gz" \
    -o /homepage.tar.gz && \
    tar -xzf /homepage.tar.gz -C / && rm /homepage.tar.gz && chmod +x /homepage 2>/dev/null || true
RUN strip /homepage 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/homepage /var/cache/homepage

FROM scratch
COPY --from=downloader /homepage /homepage
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/homepage /var/log/homepage
COPY --from=builder /var/cache/homepage /var/cache/homepage
USER 65534:65534
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/homepage", "--version"]
ENTRYPOINT ["/homepage"]
LABEL org.opencontainers.image.title="homepage" \
      org.opencontainers.image.description="Homepage - Application dashboard" \
      org.opencontainers.image.vendor="benphelps" \
      org.opencontainers.image.source="https://github.com/benphelps/homepage" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
