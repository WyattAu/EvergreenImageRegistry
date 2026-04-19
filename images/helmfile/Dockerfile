# =============================================================================
# SOVEREIGN HARDENED HELMFILE
# Generated from template - Version: 0.162.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.162.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/helmfile/helmfile/releases/download/v0.162.0/helmfile_0.162.0_linux_amd64.tar.gz" -o /helmfile.tar.gz && \
    tar -xzf /helmfile.tar.gz -C / && rm /helmfile.tar.gz && chmod +x /helmfile 2>/dev/null || \
    curl -fsSL "https://github.com/helmfile/helmfile/releases/download/v0.162.0/helmfile_0.162.0_linux_amd64.tar.gz" -o /helmfile && chmod +x /helmfile

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/helmfile /var/cache/helmfile

FROM scratch
COPY --from=downloader /helmfile /helmfile
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/helmfile /var/log/helmfile
COPY --from=builder /var/cache/helmfile /var/cache/helmfile
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/helmfile", "--version"]
ENTRYPOINT ["/helmfile"]
LABEL org.opencontainers.image.title="helmfile" \
      org.opencontainers.image.version="0.162.0" \
      org.opencontainers.image.vendor="Helmfile" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
