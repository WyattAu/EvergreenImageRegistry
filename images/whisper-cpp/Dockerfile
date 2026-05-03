ARG VERSION=1.8.4
ARG TARGETARCH

FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake g++ make git wget ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v${VERSION} \
    https://github.com/ggerganov/whisper.cpp.git /tmp/whisper.cpp
WORKDIR /tmp/whisper.cpp
RUN cmake -B build -DGGML_CUDA=OFF -DWHISPER_NO_ACCELERATE=ON && \
    cmake --build build -j$(nproc) --target whisper-cli && \
    cp /tmp/whisper.cpp/build/bin/whisper-cli /whisper-cli && chmod +x /whisper-cli

FROM debian:bookworm-slim AS builder
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
ENTRYPOINT ["/whisper-cli"]
LABEL org.opencontainers.image.title="whisper-cpp" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ggerganov/whisper.cpp" \
      org.opencontainers.image.source="https://github.com/ggerganov/whisper.cpp" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
