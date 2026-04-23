# =============================================================================
# SOVEREIGN HARDENED NETMAKER
# Generated from template - Version: 1.5.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.5.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/gravitl/netmaker/releases/download/v1.5.1/netmaker-linux-amd64" -o /netmaker.tar.gz && \
    tar -xzf /netmaker.tar.gz -C / && rm /netmaker.tar.gz && chmod +x /netmaker 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/gravitl/netmaker/releases/download/v1.5.1/netmaker-linux-amd64" -o /netmaker && chmod +x /netmaker

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/netmaker /var/cache/netmaker

FROM scratch
COPY --from=downloader /netmaker /netmaker
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/netmaker /var/log/netmaker
COPY --from=builder /var/cache/netmaker /var/cache/netmaker
USER 65532:65532
WORKDIR /app
EXPOSE 443 8080
ENTRYPOINT ["/netmaker"]
LABEL org.opencontainers.image.title="netmaker" \
      org.opencontainers.image.version="1.5.1" \
      org.opencontainers.image.vendor="NetMaker" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM