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
        curl="7.88.1-*" \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/Nheko-Reborn/nheko/releases/download/v${VERSION}/nheko-${VERSION}-x86_64-linux-gnu.AppImage" -o /tmp/nheko.AppImage && \
    chmod +x /tmp/nheko.AppImage && \
    /tmp/nheko.AppImage --appimage-extract 2>/dev/null || true

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libqt6core6="6.4.*" \
        libqt6gui6="6.4.*" \
        libqt6widgets6="6.4.*" \
        libqt6network6="6.4.*" \
        libqt6qml6="6.4.*" \
        libqt6quick6="6.4.*" \
        libqt6multimedia6="6.4.*" \
        libssl3 \
        ca-certificates \
        libgl1 \
        libglib2.0-0 \
        libcjson4 && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd -r -g 65534 nheko && useradd -r -u 65534 -g nheko -d /app -s /usr/sbin/nologin nheko
COPY --from=builder /tmp/nheko.AppImage /app/nheko
COPY --from=builder /squashfs-root/usr/bin/nheko /usr/local/bin/nheko 2>/dev/null || true
RUN mkdir -p /app /home/nheko/.config/nheko && chown -R 65534:65534 /app /home/nheko
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["nheko", "--version"]
ENTRYPOINT ["nheko"]
LABEL org.opencontainers.image.title="nheko" \
      org.opencontainers.image.description="Nheko - desktop Matrix client (Qt/C++)" \
      org.opencontainers.image.version="2.4.0" \
      org.opencontainers.image.vendor="Nheko" \
      org.opencontainers.image.source="https://github.com/Nheko-Reborn/nheko" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
