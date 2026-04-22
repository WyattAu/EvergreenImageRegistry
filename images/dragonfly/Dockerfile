# =============================================================================
# SOVEREIGN ALIAS - DRAGONFLY -> dragonflydb
# Alias for images/dragonflydb/
# =============================================================================

ARG VERSION=v1.18.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/dragonflydb/dragonfly/releases/download/${VERSION}/dragonfly-${VERSION}-linux-amd64.tar.gz" -o /dragonfly.tar.gz && \
    tar -xzf /dragonfly.tar.gz -C /tmp/ && \
    chmod +x /tmp/dragonfly && \
    mv /tmp/dragonfly /dragonfly && \
    rm -rf /dragonfly.tar.gz /tmp/*

FROM scratch
COPY --from=downloader /dragonfly /dragonfly
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 6379
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/dragonfly", "--version"]
ENTRYPOINT ["/dragonfly"]
CMD ["--bind", "0.0.0.0:6379"]
LABEL org.opencontainers.image.title="dragonfly" \
      org.opencontainers.image.version="1.18.0" \
      org.opencontainers.image.vendor="DragonflyDB" \
      org.opencontainers.image.source="https://github.com/dragonflydb/dragonfly" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
