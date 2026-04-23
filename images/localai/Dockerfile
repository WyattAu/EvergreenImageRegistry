# =============================================================================
# SOVEREIGN HARDENED LOCALAI
# Generated from template - Version: 4.1.3
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.1.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/mudler/LocalAI/releases/download/v4.1.3/local-ai-v4.1.3-linux-amd64" -o /localai.tar.gz && \
    tar -xzf /localai.tar.gz -C / && rm /localai.tar.gz && chmod +x /localai 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/mudler/LocalAI/releases/download/v4.1.3/local-ai-v4.1.3-linux-amd64" -o /localai && chmod +x /localai

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/localai /var/cache/localai

FROM scratch
COPY --from=downloader /localai /localai
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/localai /var/log/localai
COPY --from=builder /var/cache/localai /var/cache/localai
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/localai"]
LABEL org.opencontainers.image.title="localai" \
      org.opencontainers.image.version="4.1.3" \
      org.opencontainers.image.vendor="LocalAI" \
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