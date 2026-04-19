# =============================================================================
# SOVEREIGN HARDENED STEP-CLI
# Generated from template - Version: 0.25.2
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.25.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/smallstep/cli/releases/download/v0.25.2/step_0.25.2_linux_amd64.tar.gz" -o /step.tar.gz && \
    tar -xzf /step.tar.gz -C / && rm /step.tar.gz && chmod +x /step 2>/dev/null || \
    curl -fsSL "https://github.com/smallstep/cli/releases/download/v0.25.2/step_0.25.2_linux_amd64.tar.gz" -o /step && chmod +x /step

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/step /var/cache/step

FROM scratch
COPY --from=downloader /step /step
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/step /var/log/step
COPY --from=builder /var/cache/step /var/cache/step
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD step step version
ENTRYPOINT ["/step"]
LABEL org.opencontainers.image.title="step-cli" \
      org.opencontainers.image.version="0.25.2" \
      org.opencontainers.image.vendor="Smallstep" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
