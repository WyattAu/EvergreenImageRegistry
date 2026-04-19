# =============================================================================
# SOVEREIGN HARDENED PORTAINER
# Generated from template - Version: 2.20.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.20.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/portainer/portainer/releases/download/2.20.1/portainer-2.20.1-linux-amd64.tar.gz" -o /portainer.tar.gz && \
    tar -xzf /portainer.tar.gz -C / && rm /portainer.tar.gz && chmod +x /portainer 2>/dev/null || \
    curl -fsSL "https://github.com/portainer/portainer/releases/download/2.20.1/portainer-2.20.1-linux-amd64.tar.gz" -o /portainer && chmod +x /portainer

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/portainer /var/cache/portainer

FROM scratch
COPY --from=downloader /portainer /portainer
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/portainer /var/log/portainer
COPY --from=builder /var/cache/portainer /var/cache/portainer
USER 65534:65534
WORKDIR /app
EXPOSE 9000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/portainer", "--version"]
ENTRYPOINT ["/portainer"]
LABEL org.opencontainers.image.title="portainer" \
      org.opencontainers.image.version="2.20.1" \
      org.opencontainers.image.vendor="Portainer" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
