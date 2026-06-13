







ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG VERSION=b5415
ARG TARGETARCH







RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/ggml-org/llama.cpp/releases/download/b5415/llama-b5415-bin-ubuntu-x64.zip -o /llama-server \
    echo "a0d6087a0fdfc94b97a523e9761ec7dffe78bd28bc345da9e0d834b03fe20013  /llama-server" | sha256sum -c  #































FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /app /var/log/llama-cpp-server /var/cache/llama-cpp-server 2>/dev/null || true























FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim








COPY --from=downloader /llama-server /llama-server







COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt







COPY --from=builder /app /app







COPY --from=builder /var/log/llama-cpp-server /var/log/llama-cpp-server







COPY --from=builder /var/cache/llama-cpp-server /var/cache/llama-cpp-server







USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"







WORKDIR /app







EXPOSE 8080






















HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]







LABEL org.opencontainers.image.title="llama-cpp-server" \
      org.opencontainers.image.description="llama-cpp-server container image" \
      org.opencontainers.image.version="b5415" \
      org.opencontainers.image.vendor="ggerganov/llama.cpp" \
      org.opencontainers.image.source="https://github.com/ggerganov/llama.cpp/releases" \
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







LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
