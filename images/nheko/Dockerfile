# =============================================================================
# SOVEREIGN HARDENED NHEKO
# Constraint: debian-slim - Qt/C++ runtime libraries required
# =============================================================================

ARG VERSION=2.4.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Nheko-Reborn/nheko/releases/download/v${VERSION}/nheko-${VERSION}-x86_64-linux-gnu.AppImage" -o /tmp/nheko.AppImage && \
    chmod +x /tmp/nheko.AppImage && \
    /tmp/nheko.AppImage --appimage-extract 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apk add --no-cache ca-certificates glib
RUN addgroup -S -g 65532 nheko && adduser -u 65532 -G nheko -D -h /app -s /sbin/nologin nheko
COPY --from=builder /tmp/nheko.AppImage /app/nheko
COPY --from=builder /squashfs-root/usr/bin/nheko /usr/local/bin/nheko 2>/dev/null || true
RUN mkdir -p /app /home/nheko/.config/nheko && chown -R 65532:65532 /app /home/nheko
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["nheko"]
LABEL org.opencontainers.image.title="nheko" \
      org.opencontainers.image.description="Nheko - desktop Matrix client (Qt/C++)" \
      org.opencontainers.image.version="2.4.0" \
      org.opencontainers.image.vendor="Nheko" \
      org.opencontainers.image.source="https://github.com/Nheko-Reborn/nheko" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM