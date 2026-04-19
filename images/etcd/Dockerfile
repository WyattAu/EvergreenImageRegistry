# =============================================================================
# SOVEREIGN HARDENED ETCD
# Generated from template - Version: 3.5.15
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.5.15
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/etcd-io/etcd/releases/download/v3.5.15/etcd-3.5.15-linux-amd64.tar.gz" -o /etcd.tar.gz && \
    tar -xzf /etcd.tar.gz -C / && rm /etcd.tar.gz && chmod +x /etcd 2>/dev/null || \
    curl -fsSL "https://github.com/etcd-io/etcd/releases/download/v3.5.15/etcd-3.5.15-linux-amd64.tar.gz" -o /etcd && chmod +x /etcd

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/etcd /var/cache/etcd

FROM scratch
COPY --from=downloader /etcd /etcd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/etcd /var/log/etcd
COPY --from=builder /var/cache/etcd /var/cache/etcd
USER 65534:65534
WORKDIR /app
EXPOSE 2379 2380
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/etcd", "--version"]
ENTRYPOINT ["/etcd"]
LABEL org.opencontainers.image.title="etcd" \
      org.opencontainers.image.version="3.5.15" \
      org.opencontainers.image.vendor="etcd" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
