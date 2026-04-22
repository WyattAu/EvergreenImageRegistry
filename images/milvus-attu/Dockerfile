# =============================================================================
# SOVEREIGN HARDENED MILVUS-ATTU
# Generated from template - Version: 2.4.9
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.4.9
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/zilliztech/attu/releases/download/v2.4.9/attu-v2.4.9-linux-x64.tar.gz" -o /attu.tar.gz && \
    tar -xzf /attu.tar.gz -C / && rm /attu.tar.gz && chmod +x /attu 2>/dev/null || \
    curl -fsSL "https://github.com/zilliztech/attu/releases/download/v2.4.9/attu-v2.4.9-linux-x64.tar.gz" -o /attu && chmod +x /attu

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/milvus-attu /var/cache/milvus-attu

FROM scratch
COPY --from=downloader /attu /attu
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/milvus-attu /var/log/milvus-attu
COPY --from=builder /var/cache/milvus-attu /var/cache/milvus-attu
USER 65534:65534
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/attu", "--version"]
ENTRYPOINT ["/attu"]
LABEL org.opencontainers.image.title="milvus-attu" \
      org.opencontainers.image.version="2.4.9" \
      org.opencontainers.image.vendor="zilliztech/attu" \
      org.opencontainers.image.source="https://github.com/zilliztech/attu/releases/download/v2.4.9" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
