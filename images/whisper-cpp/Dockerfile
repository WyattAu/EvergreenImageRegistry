# =============================================================================
# SOVEREIGN HARDENED WHISPER-CPP
# Generated from template - Version: 1.6.2
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.6.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/ggerganov/whisper.cpp/releases/download/v1.6.2/whisper-1.6.2-bin-x64.tar.gz" -o /whisper-cli && chmod +x /whisper-cli

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/whisper-cpp /var/cache/whisper-cpp

FROM scratch
COPY --from=downloader /whisper-cli /whisper-cli
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/whisper-cpp /var/log/whisper-cpp
COPY --from=builder /var/cache/whisper-cpp /var/cache/whisper-cpp
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/whisper-cli", "--help"]
ENTRYPOINT ["/whisper-cli"]
LABEL org.opencontainers.image.title="whisper-cpp" \
      org.opencontainers.image.version="1.6.2" \
      org.opencontainers.image.vendor="ggerganov/whisper.cpp" \
      org.opencontainers.image.source="https://github.com/ggerganov/whisper.cpp/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
