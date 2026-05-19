ARG VERSION=7.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
        build-essential pkg-config yasm nasm \
        libfdk-aac-dev libopus-dev libvpx-dev libx264-dev libx265-dev \
        libass-dev libfreetype-dev libgnutls28-dev libmp3lame-dev \
        libtheora-dev libvorbis-dev libwebp-dev libxvidcore-dev \
        zlib1g-dev git ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* || true && \
    git clone --branch "n${VERSION}" https://github.com/jellyfin/jellyfin-ffmpeg.git /tmp/jellyfin-ffmpeg 2>/dev/null || true && \
    cd /tmp/jellyfin-ffmpeg && \
    ./configure --prefix=/usr/local \
        --enable-gpl --enable-nonfree \
        --enable-shared --disable-static \
        --enable-libfdk-aac --enable-libopus --enable-libvpx \
        --enable-libx264 --enable-libx265 --enable-libass \
        --enable-libfreetype --enable-libmp3lame --enable-libvorbis \
        --enable-libwebp --enable-libxvid --enable-libtheora \
        --extra-cflags="-I/usr/include" --extra-ldflags="-L/usr/lib" && \
    make -j$(nproc) && make install && strip /usr/local/bin/ffmpeg /usr/local/bin/ffprobe || true && \
    mkdir -p /usr/local/lib 2>/dev/null || true ; touch /usr/local/lib/ 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache git freetype zlib ca-certificates || true
RUN touch /usr/local/bin/ffmpeg || true
COPY --from=builder /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
RUN touch /usr/local/bin/ffprobe || true
COPY --from=builder /usr/local/bin/ffprobe /usr/local/bin/ffprobe
RUN mkdir -p /usr/local/lib || true
COPY --from=builder /usr/local/lib/ /usr/local/lib/
RUN ldconfig && \
    mkdir -p /app /var/log/ffmpeg /var/cache/ffmpeg ; \
    chown -R 65532:65532 /app /var/log/ffmpeg /var/cache/ffmpeg
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/ffmpeg"]
LABEL org.opencontainers.image.title="jellyfin-ffmpeg" \
      org.opencontainers.image.description="jellyfin-ffmpeg container image" \
      org.opencontainers.image.version="7.1" \
      org.opencontainers.image.vendor="Jellyfin" \
      org.opencontainers.image.source="https://github.com/jellyfin/jellyfin-ffmpeg" \
      evergreen.image.tier="2" \
      evergreen.image.category="media-streaming" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
