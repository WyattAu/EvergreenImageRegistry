ARG VERSION=v1.33.6+k3s1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/k3s-io/k3s/releases/download/v1.33.6+k3s1/k3s" -o /k3s && \
    chmod +x /k3s && strip /k3s

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/k3s-agent /var/cache/k3s-agent /var/lib/rancher/k3s/agent

FROM scratch
COPY --from=downloader /k3s /k3s
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/k3s-agent /var/log/k3s-agent
COPY --from=builder /var/cache/k3s-agent /var/cache/k3s-agent
COPY --from=builder /var/lib/rancher/k3s/agent /var/lib/rancher/k3s/agent
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/k3s", "--version"]
ENTRYPOINT ["/k3s", "agent"]
LABEL org.opencontainers.image.title="k3s-agent" \
      org.opencontainers.image.version="1.33.6+k3s1" \
      org.opencontainers.image.vendor="SUSE" \
      org.opencontainers.image.description="Sovereign hardened k3s-agent - K3s agent mode" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s"
