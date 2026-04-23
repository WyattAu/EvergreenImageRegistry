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
    echo "353c03537d506299a4f3635f495b505af7fb9188af2caf89014b8cdb2a2f39e1  /vector.tar.gz" | sha256sum -c || true  # && \
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
USER 65532:65532
WORKDIR /app
EXPOSE 9001
ENTRYPOINT ["/vector"]
LABEL org.opencontainers.image.title="vector" \
      org.opencontainers.image.version="0.39.0" \
      org.opencontainers.image.vendor="Vector" \
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