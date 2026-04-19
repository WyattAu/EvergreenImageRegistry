# =============================================================================
# SOVEREIGN HARDENED VECTOR
# Generated from template - Version: 0.39.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.39.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/vectordotdev/vector/releases/download/v0.39.0/vector-0.39.0-x86_64-unknown-linux-musl.tar.gz" -o /vector.tar.gz && \
    tar -xzf /vector.tar.gz -C / && rm /vector.tar.gz && chmod +x /vector 2>/dev/null || \
    curl -fsSL "https://github.com/vectordotdev/vector/releases/download/v0.39.0/vector-0.39.0-x86_64-unknown-linux-musl.tar.gz" -o /vector && chmod +x /vector

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/vector /var/cache/vector

FROM scratch
COPY --from=downloader /vector /vector
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vector /var/log/vector
COPY --from=builder /var/cache/vector /var/cache/vector
USER 65534:65534
WORKDIR /app
EXPOSE 9001
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/vector", "--version"]
ENTRYPOINT ["/vector"]
LABEL org.opencontainers.image.title="vector" \
      org.opencontainers.image.version="0.39.0" \
      org.opencontainers.image.vendor="Vector" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
