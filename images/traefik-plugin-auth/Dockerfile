# =============================================================================
# SOVEREIGN HARDENED TRAEFIK-PLUGIN-AUTH
# Generated from template - Version: 3.6.13
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.6.13
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/traefik/traefik/releases/download/v3.6.13/traefik_v3.6.13_linux_amd64.tar.gz" -o /traefik.tar.gz && \
    echo "85fcf245e963293ca6afee4180f6116b97004499b584ebfbc2c5841e1c8d4399  /traefik.tar.gz" | sha256sum -c - && \
    tar -xzf /traefik.tar.gz -C / && rm /traefik.tar.gz && chmod +x /traefik 2>/dev/null || \
    curl -fsSL "https://github.com/traefik/traefik/releases/download/v3.6.13/traefik_v3.6.13_linux_amd64.tar.gz" -o /traefik && chmod +x /traefik

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/traefik /var/cache/traefik

FROM scratch
COPY --from=downloader /traefik /traefik
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/traefik /var/log/traefik
COPY --from=builder /var/cache/traefik /var/cache/traefik
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/traefik", "version"]
ENTRYPOINT ["/traefik"]
LABEL org.opencontainers.image.title="traefik-plugin-auth" \
      org.opencontainers.image.version="3.6.13" \
      org.opencontainers.image.vendor="Traefik Labs" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
