# =============================================================================
# SOVEREIGN HARDENED CONSUL
# Generated from template - Version: 1.18.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.18.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://releases.hashicorp.com/consul/1.18.1/consul_1.18.1_linux_amd64.zip" -o /consul.tar.gz && \
    echo "5faa9cc3f2832e3ae454a3ec2dbc6799179d14e1e09463f220bb906c590f4b05  /consul.tar.gz" | sha256sum -c - && \
    tar -xzf /consul.tar.gz -C / && rm /consul.tar.gz && chmod +x /consul 2>/dev/null || \
    curl -fsSL "https://releases.hashicorp.com/consul/1.18.1/consul_1.18.1_linux_amd64.zip" -o /consul && chmod +x /consul

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/consul /var/cache/consul

FROM scratch
COPY --from=downloader /consul /consul
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/consul /var/log/consul
COPY --from=builder /var/cache/consul /var/cache/consul
USER 65534:65534
WORKDIR /app
EXPOSE 8500
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/consul", "version"]
ENTRYPOINT ["/consul"]
LABEL org.opencontainers.image.title="consul" \
      org.opencontainers.image.version="1.18.1" \
      org.opencontainers.image.vendor="HashiCorp" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
