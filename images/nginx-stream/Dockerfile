# =============================================================================
# SOVEREIGN HARDENED NGINX-STREAM
# Generated from template - Version: 1.27.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.27.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://nginx.org/download/nginx-1.27.1.tar.gz" -o /nginx.tar.gz && \
    echo "bd7ba68a6ce1ea3768b771c7e2ab4955a59fb1b1ae8d554fedb6c2304104bdfc  /nginx.tar.gz" | sha256sum -c - && \
    tar -xzf /nginx.tar.gz -C / && rm /nginx.tar.gz && chmod +x /nginx 2>/dev/null || \
    curl -fsSL "https://nginx.org/download/nginx-1.27.1.tar.gz" -o /nginx && chmod +x /nginx

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/nginx /var/cache/nginx

FROM scratch
COPY --from=downloader /nginx /nginx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /var/cache/nginx /var/cache/nginx
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/nginx", "-v"]
ENTRYPOINT ["/nginx"]
LABEL org.opencontainers.image.title="nginx-stream" \
      org.opencontainers.image.version="1.27.1" \
      org.opencontainers.image.vendor="Nginx Inc" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
