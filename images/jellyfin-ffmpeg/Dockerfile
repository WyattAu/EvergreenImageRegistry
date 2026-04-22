ARG VERSION=7.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential pkg-config yasm nasm \
        libfdk-aac-dev libopus-dev libvpx-dev libx264-dev libx265-dev \
        libass-dev libfreetype-dev libgnutls28-dev libmp3lame-dev \
        libtheora-dev libvorbis-dev libwebp-dev libxvidcore-dev \
        zlib1g-dev ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch n{version} \
    "https://github.com/jellyfin/jellyfin-ffmpeg.git" /tmp/jellyfin-ffmpeg && \
    cd /tmp/jellyfin-ffmpeg && \
    ./configure --prefix=/usr/local \
        --enable-gpl --enable-nonfree \
        --enable-shared --disable-static \
        --enable-libfdk-aac --enable-libopus --enable-libvpx \
        --enable-libx264 --enable-libx265 --enable-libass \
        --enable-libfreetype --enable-libmp3lame --enable-libvorbis \
        --enable-libwebp --enable-libxvid --enable-libtheora \
        --extra-cflags="-I/usr/include" --extra-ldflags="-L/usr/lib" && \
    make -j$(nproc) && make install && strip /usr/local/bin/ffmpeg /usr/local/bin/ffprobe

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        libfdk-acct2 libopus0 libvpx7 libx264-164 libx265-199 \
        libass9 libfreetype6 libmp3lame0 libvorbis0a libwebp7 \
        libxvidcore4 libtheora0 zlib1g ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
COPY --from=builder /usr/local/bin/ffprobe /usr/local/bin/ffprobe
COPY --from=builder /usr/local/lib/ /usr/local/lib/
RUN ldconfig && \
    mkdir -p /app /var/log/ffmpeg /var/cache/ffmpeg && \
    chown -R 65534:65534 /app /var/log/ffmpeg /var/cache/ffmpeg
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/ffmpeg", "-version"]
ENTRYPOINT ["/usr/local/bin/ffmpeg"]
LABEL org.opencontainers.image.title="jellyfin-ffmpeg" \
      org.opencontainers.image.version="7.1" \
      org.opencontainers.image.vendor="Jellyfin" \
      org.opencontainers.image.source="https://github.com/jellyfin/jellyfin-ffmpeg" \
      sovereign.image.tier="2" \
      sovereign.image.category="media-streaming" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
