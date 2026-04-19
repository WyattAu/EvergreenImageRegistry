# =============================================================================
# SOVEREIGN HARDENED HOMEPAGE
# Generated from template - Version: 0.8.18
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.8.18
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/benphelps/homepage/releases/download/v0.8.18/homepage-0.8.18-linux-amd64.tar.gz" -o /homepage.tar.gz && \
    tar -xzf /homepage.tar.gz -C / && rm /homepage.tar.gz && chmod +x /homepage 2>/dev/null || \
    curl -fsSL "https://github.com/benphelps/homepage/releases/download/v0.8.18/homepage-0.8.18-linux-amd64.tar.gz" -o /homepage && chmod +x /homepage

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
      org.opencontainers.image.version="0.8.18" \
      org.opencontainers.image.vendor="Homepage" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
