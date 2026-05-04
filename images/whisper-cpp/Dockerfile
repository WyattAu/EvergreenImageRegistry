ARG VERSION=1.8.4
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake g++ make git wget ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --depth 1 --branch v${VERSION} \
    https://github.com/ggerganov/whisper.cpp.git /tmp/whisper.cpp
WORKDIR /tmp/whisper.cpp
RUN cmake -B build -DGGML_CUDA=OFF -DWHISPER_NO_ACCELERATE=ON && \
    cmake --build build -j$(nproc) --target whisper-cli && \
    cp /tmp/whisper.cpp/build/bin/whisper-cli /whisper-cli && chmod +x /whisper-cli

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/whisper-cpp /var/cache/whisper-cpp 2>/dev/null || true

FROM scratch
COPY --from=builder /whisper-cli /whisper-cli
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/whisper-cpp /var/log/whisper-cpp
COPY --from=builder /var/cache/whisper-cpp /var/cache/whisper-cpp
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/whisper-cli"]
LABEL org.opencontainers.image.title="whisper-cpp" \
      org.opencontainers.image.description="whisper-cpp container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ggerganov/whisper.cpp" \
      org.opencontainers.image.source="https://github.com/ggerganov/whisper.cpp" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
