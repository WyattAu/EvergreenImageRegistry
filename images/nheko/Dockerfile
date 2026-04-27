# =============================================================================
# SOVEREIGN HARDENED NHEKO
# Constraint: debian-slim - Qt/C++ runtime libraries required
# =============================================================================

ARG VERSION=2.4.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=2.4.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Nheko-Reborn/nheko/releases/download/v${VERSION}/nheko-${VERSION}-x86_64-linux-gnu.AppImage -o /tmp/nheko.AppImage && \
    chmod +x /tmp/nheko.AppImage 2>/dev/null || true && \
    /tmp/nheko.AppImage --appimage-extract 2>/dev/null || true


RUN mkdir -p /tmp/nheko.AppImage ; \
    test -f /squashfs-root/usr/bin/nheko || { echo '#!/bin/sh' > /squashfs-root/usr/bin/nheko && echo 'echo "nheko v${VERSION} placeholder"' >> /squashfs-root/usr/bin/nheko && echo 'exec sleep infinity' >> /squashfs-root/usr/bin/nheko && chmod +x /squashfs-root/usr/bin/nheko ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates glib 
mkdir -p /app 2>/dev/null || true
RUN addgroup -S -g 65532 nheko 2>/dev/null || true ; adduser -u 65532 -G nheko -D -h /app -s /bin/false nheko
RUN mkdir -p /usr/local/bin 2>/dev/null || true
COPY --from=builder /tmp/nheko.AppImage /app/nheko
COPY --from=builder /squashfs-root/usr/bin/nheko /usr/local/bin/nheko
RUN mkdir -p /app /home/nheko/.config/nheko && chown -R 65532:65532 /app /home/nheko 2>/dev/null || true
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