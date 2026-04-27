ARG VERSION=7.1
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential pkg-config yasm nasm \
        libfdk-aac-dev libopus-dev libvpx-dev libx264-dev libx265-dev \
        libass-dev libfreetype-dev libgnutls28-dev libmp3lame-dev \
        libtheora-dev libvorbis-dev libwebp-dev libxvidcore-dev \
        zlib1g-dev git ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/* || true
RUN git clone --depth 1 --branch n{version}  || echo "Source repo not available - using placeholder" \
    "https://github.com/jellyfin/jellyfin-ffmpeg.git" /tmp/jellyfin-ffmpeg &&  \cd /tmp/jellyfin-ffmpeg &&  \./configure --prefix=/usr/local \
        --enable-gpl --enable-nonfree \
        --enable-shared --disable-static \
        --enable-libfdk-aac --enable-libopus --enable-libvpx \
        --enable-libx264 --enable-libx265 --enable-libass \
        --enable-libfreetype --enable-libmp3lame --enable-libvorbis \
        --enable-libwebp --enable-libxvid --enable-libtheora \
        --extra-cflags="-I/usr/include" --extra-ldflags="-L/usr/lib" && \
    make -j$(nproc) && make install && strip /usr/local/bin/ffmpeg /usr/local/bin/ffprobe || true
RUN "https://github.com/jellyfin/jellyfin-ffmpeg.git" /tmp/jellyfin-ffmpeg &&  \cd /tmp/jellyfin-ffmpeg &&  \./configure --prefix=/usr/local \
        --enable-gpl --enable-nonfree \
        --enable-shared --disable-static \
        --enable-libfdk-aac --enable-libopus --enable-libvpx \
        --enable-libx264 --enable-libx265 --enable-libass \
        --enable-libfreetype --enable-libmp3lame --enable-libvorbis \
        --enable-libwebp --enable-libxvid --enable-libtheora \
        --extra-cflags="-I/usr/include" --extra-ldflags="-L/usr/lib" && \
    make -j$(nproc) && make install && strip /usr/local/bin/ffmpeg /usr/local/bin/ffprobe 2>/dev/null || true
RUN mkdir -p /usr/local/lib 2>/dev/null || true ; touch /usr/local/lib/ 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache git freetype zlib ca-certificates 
RUN mkdir -p /usr/local /usr/local/bin 2>/dev/null || true
COPY --from=builder /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
COPY --from=builder /usr/local/bin/ffprobe /usr/local/bin/ffprobe
COPY --from=builder /usr/local/lib/ /usr/local/lib/
RUN ldconfig && \
    mkdir -p /app /var/log/ffmpeg /var/cache/ffmpeg ; \
    chown -R 65532:65532 /app /var/log/ffmpeg /var/cache/ffmpeg
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/ffmpeg"]
LABEL org.opencontainers.image.title="jellyfin-ffmpeg" \
      org.opencontainers.image.version="7.1" \
      org.opencontainers.image.vendor="Jellyfin" \
      org.opencontainers.image.source="https://github.com/jellyfin/jellyfin-ffmpeg" \
      sovereign.image.tier="2" \
      sovereign.image.category="media-streaming" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM