# =============================================================================
# SOVEREIGN HARDENED KANIKO
# Generated from template - Version: 1.24.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
#
# NOTE: Kaniko does not provide standalone binary releases.
# Binary is extracted from the official kaniko executor container image.
# =============================================================================

ARG VERSION=1.24.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates skopeo && rm -rf /var/lib/apt/lists/*
RUN skopeo copy "docker://gcr.io/kaniko-project/executor:v${VERSION}" "dir:/tmp/kaniko-image" && \
    cp /tmp/kaniko-image/kaniko/executor /kaniko && chmod +x /kaniko && rm -rf /tmp/kaniko-image

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kaniko /var/cache/kaniko

FROM scratch
COPY --from=downloader /kaniko /kaniko
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kaniko /var/log/kaniko
COPY --from=builder /var/cache/kaniko /var/cache/kaniko
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/kaniko", "--version"]
ENTRYPOINT ["/kaniko"]
LABEL org.opencontainers.image.title="kaniko" \
      org.opencontainers.image.version="1.24.0" \
      org.opencontainers.image.vendor="Google" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
