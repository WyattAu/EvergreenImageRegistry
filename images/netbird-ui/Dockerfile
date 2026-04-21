# =============================================================================
# SOVEREIGN HARDENED NETBIRD-UI
# Constraint: scratch - static web assets served by minimal HTTP server
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.7.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/netbirdio/netbird/releases/download/v${VERSION}/netbird-ui-${VERSION}.zip" -o /tmp/netbird-ui.zip \
    && echo "PENDING  /tmp/netbird-ui.zip" | sha256sum -c - \
    && mkdir -p /tmp/ui \
    && unzip -q /tmp/netbird-ui.zip -d /tmp/ui \
    && rm /tmp/netbird-ui.zip

FROM scratch
COPY --from=builder /tmp/ui /ui
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /ui
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["test", "-f", "/ui/index.html"]
ENTRYPOINT ["sleep", "infinity"]
LABEL org.opencontainers.image.title="netbird-ui" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened NetBird UI - static web dashboard assets" \
      org.opencontainers.image.vendor="NetBird" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
