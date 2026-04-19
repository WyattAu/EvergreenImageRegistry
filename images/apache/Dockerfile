# =============================================================================
# SOVEREIGN HARDENED APACHE
# Generated from template - Version: 2.4.61
# Constraint: distroless/static - no shell, no package manager
# =============================================================================

ARG VERSION=2.4.61
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://httpd.apache.org/" -o /httpd.tar.gz && \
    tar -xzf /httpd.tar.gz -C / && rm /httpd.tar.gz && chmod +x /httpd

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/httpd /var/cache/httpd

FROM gcr.io/distroless/static:nonroot@sha256:64c43684e6d2b581d1eb362ea47b6a4defee6a9cac5f7ebbda3daa67e8c9b8e6
COPY --from=downloader /httpd /httpd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/httpd /var/log/httpd
COPY --from=builder /var/cache/httpd /var/cache/httpd
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/httpd", "-v"]
ENTRYPOINT ["/httpd"]
LABEL org.opencontainers.image.title="apache" \
      org.opencontainers.image.version="2.4.61" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
