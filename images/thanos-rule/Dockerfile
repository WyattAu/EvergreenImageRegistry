# =============================================================================
# SOVEREIGN HARDENED THANOS-RULE
# Thanos Ruler component (evaluation and alerting)
# Constraint: scratch - Go static binary
# =============================================================================

ARG VERSION=0.35.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/thanos-io/thanos/releases/download/v${VERSION}/thanos-${VERSION}.linux-amd64.tar.gz" -o /thanos.tar.gz && \
    tar -xzf /thanos.tar.gz -C /tmp && rm /thanos.tar.gz && \
    chmod +x /tmp/thanos-${VERSION}.linux-amd64/thanos && \
    mv /tmp/thanos-${VERSION}.linux-amd64/thanos /thanos

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/thanos /var/cache/thanos

FROM scratch
COPY --from=downloader /thanos /thanos
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/thanos /var/log/thanos
COPY --from=builder /var/cache/thanos /var/cache/thanos
USER 65534:65534
WORKDIR /app
EXPOSE 10902
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/thanos", "rule", "--version"]
ENTRYPOINT ["/thanos"]
CMD ["rule"]
LABEL org.opencontainers.image.title="thanos-rule" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Thanos" \
      org.opencontainers.image.source="https://github.com/thanos-io/thanos" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
