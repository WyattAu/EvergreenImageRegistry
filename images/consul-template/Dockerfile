# =============================================================================
# SOVEREIGN HARDENED CONSUL-TEMPLATE
# Generated from template - Version: 0.37.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.37.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://releases.hashicorp.com/consul-template/0.37.0/consul-template_0.37.0_linux_amd64.zip" -o /consul-template.tar.gz && \
    tar -xzf /consul-template.tar.gz -C / && rm /consul-template.tar.gz && chmod +x /consul-template 2>/dev/null || \
    curl -fsSL "https://releases.hashicorp.com/consul-template/0.37.0/consul-template_0.37.0_linux_amd64.zip" -o /consul-template && chmod +x /consul-template

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/consul-template /var/cache/consul-template

FROM scratch
COPY --from=downloader /consul-template /consul-template
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/consul-template /var/log/consul-template
COPY --from=builder /var/cache/consul-template /var/cache/consul-template
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD consul-template consul-template --version
ENTRYPOINT ["/consul-template"]
LABEL org.opencontainers.image.title="consul-template" \
      org.opencontainers.image.version="0.37.0" \
      org.opencontainers.image.vendor="HashiCorp" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
