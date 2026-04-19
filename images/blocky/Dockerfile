# =============================================================================
# SOVEREIGN HARDENED BLOCKY
# Generated from template - Version: 0.22
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.22
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/0xERR0R/blocky/releases/download/v0.22/blocky_0.22_linux_amd64.tar.gz" -o /blocky.tar.gz && \
    tar -xzf /blocky.tar.gz -C / && rm /blocky.tar.gz && chmod +x /blocky 2>/dev/null || \
    curl -fsSL "https://github.com/0xERR0R/blocky/releases/download/v0.22/blocky_0.22_linux_amd64.tar.gz" -o /blocky && chmod +x /blocky

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/blocky /var/cache/blocky

FROM scratch
COPY --from=downloader /blocky /blocky
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/blocky /var/log/blocky
COPY --from=builder /var/cache/blocky /var/cache/blocky
USER 65534:65534
WORKDIR /app
EXPOSE 53 4000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD blocky blocky --version
ENTRYPOINT ["/blocky"]
LABEL org.opencontainers.image.title="blocky" \
      org.opencontainers.image.version="0.22" \
      org.opencontainers.image.vendor="Blocky" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
